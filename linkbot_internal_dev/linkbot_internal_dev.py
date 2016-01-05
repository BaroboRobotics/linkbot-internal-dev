#!/usr/bin/env python3

__version__ = "0.0.1"

import sqlite3 as sql
from PyQt4 import QtCore, QtGui

try:
    from linkbot_internal_dev.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow

try:
    import linkbot_internal_dev.preassembly as preassembly
except:
    import preassembly

try: 
    from linkbot_internal_dev import tests 
except:
    import tests 

#import linkbot_diagnostics as diagnostics
from linkbot_diagnostics.LinkbotDiagnosticGui import initialize_tables
from linkbot_diagnostics.LinkbotDiagnosticGui import LinkbotDiagnostic 
from linkbot_diagnostics.testlinkbot import TestLinkbot

import linkbot
import threading
import sys
import time
import traceback
import os
import appdirs

db_dir = os.path.join(appdirs.user_data_dir(), "linkbot-diagnostics")
db_file = os.path.join(db_dir, "database.db")

class StartQT4(QtGui.QMainWindow):
    diagnostics_finished = QtCore.pyqtSignal(int)
    diagnostics_error = QtCore.pyqtSignal(str, str) # (title, message)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Linkbot Testing Suite ' + __version__)

        self.checkboxes = [ self.ui.checkBox_accelerometer,
                            self.ui.checkBox_button,
                            self.ui.checkBox_buzzer,
                            self.ui.checkBox_calibration,
                            self.ui.checkBox_led,
                            self.ui.checkBox_motor_test,
                            self.ui.checkBox_radio,
                            self.ui.checkBox_serial_id,
                          ]

        self.tests = [ (tests.Start, None),
                       (tests.SerialId, self.ui.checkBox_serial_id),
                       (tests.Radio, self.ui.checkBox_radio),
                       (tests.Final, None),
                     ]

        self._tests = iter(self.tests)
        self._test = None
        self._test_widget = None

        self.display_next_test()

    def display_next_test(self):
        try:
            if self._test[1] is not None:
                self._test[1].setChecked(True)
        except Exception as e:
            print('While trying to set checkbox:', e)

        if self._test_widget is not None:
            self.ui.test_content_layout.removeWidget(self._test_widget)
            self._test_widget.hide()
            del self._test_widget
        try:
            self._test = next(self._tests)
        except StopIteration:
            for b in self.checkboxes:
                b.setChecked(False)
            self._tests = iter(self.tests)
            self._test = next(self._tests)

        self._test_widget = self._test[0](self)
        self._test_widget.completed.connect(self.display_next_test)

        self.ui.test_content_layout.addWidget(self._test_widget)

    def message_box(self, title, message):
        QtGui.QMessageBox.information(self, title, message)

    def start_diagnostics(self):
        self.ui.groupBox.setEnabled(False)
        self.ui.groupBox_serialId.setEnabled(False)
        self.ui.pushButton_postassembly_start.setEnabled(False)
        self.ui.label_diagnostics_status.setText('Testing...')
        self.ui.label_diagnostics_status.setStyleSheet(
                'background-color: rgb(255, 255, 0);')

        self.diag_thread = threading.Thread(target=self._diagnostics)
        self.diag_thread.start()

    def end_diagnostics(self, success):
        self.ui.groupBox.setEnabled(True)
        self.ui.groupBox_serialId.setEnabled(True)
        self.ui.pushButton_postassembly_start.setEnabled(True)
        if success:
            self.ui.label_diagnostics_status.setText("Pass")
            self.ui.label_diagnostics_status.setStyleSheet(
                    'background-color: rgb(0, 255, 0);')
        else:
            self.ui.label_diagnostics_status.setText("Fail")
            self.ui.label_diagnostics_status.setStyleSheet(
                    'background-color: rgb(255, 0, 0);')

    def _diagnostics(self):
        try:
            l = TestLinkbot('LOCL')
            x,y,z = l.getAccelerometer()
            if abs(x) > 0.1 or \
               abs(x) > 0.1 or \
               abs(z-1) > 0.1:
                 self.diagnostics_error.emit('Warning',
                         'Accelerometer readings have anomalies!')
            global db_file
            con = sql.connect(db_file)
            initialize_tables(con.cursor())
            cur = con.cursor()
# Check to see if this l is in our database already. Add it if not
            cur.execute('SELECT * FROM robot_type WHERE Id=\'{}\''.format(l.getSerialId()))
            rows = cur.fetchall()
            formFactor = None
            if l.getFormFactor() == linkbot.Linkbot.FormFactor.I:
                formFactor = "linkbot.Linkbot-I"
                motor2index = 2
            elif l.getFormFactor() == linkbot.Linkbot.FormFactor.L:
                formFactor = "linkbot.Linkbot-L"
                motor2index = 1
            else:
                formFactor = "UNKNOWN"
            print ("Testing LinkBot {}".format(l.getSerialId()))
            d = LinkbotDiagnostic(l)
            results = d.runLinearityTest()
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            if len(rows) == 0:
                cur.execute('INSERT INTO robot_type VALUES(\'{}\', \'{}\')'.format(
                    l.getSerialId(), formFactor))
            cur.execute("INSERT INTO linearity_tests "
                "VALUES('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(
                    l.getSerialId(),
                    now,
                    results[0]['forward_slope'],
                    results[0]['forward_rvalue'],
                    results[0]['backward_slope'],
                    results[0]['backward_rvalue'],
                    results[motor2index]['forward_slope'],
                    results[motor2index]['forward_rvalue'],
                    results[motor2index]['backward_slope'],
                    results[motor2index]['backward_rvalue']))

            con.commit()
            con.close()
            speeds = [ 
                        results[0]['forward_slope'],
                        results[0]['backward_slope'],
                        results[motor2index]['forward_slope'],
                        results[motor2index]['backward_slope'],
                     ]
            linearities = [
                results[0]['forward_rvalue'],
                results[0]['backward_rvalue'],
                results[motor2index]['forward_rvalue'],
                results[motor2index]['backward_rvalue'],
                          ]
            if any(abs(x) < 210 for x in speeds):
                self.diagnostics_finished.emit(0)
            elif any(x < 0.93 for x in linearities):
                self.diagnostics_finished.emit(0)
            else:
                self.diagnostics_finished.emit(1)

        except Exception as e:
            self.diagnostics_error.emit('Warning',
                    "Test Failed: " + str(e))
            self.diagnostics_finished.emit(0)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
