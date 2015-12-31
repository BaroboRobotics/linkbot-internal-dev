#!/usr/bin/env python3

__version__ = "0.0.1"

from PyQt4 import QtCore, QtGui

try:
    from linkbot_internal_dev.mainwindow import Ui_MainWindow
except:
    from mainwindow import Ui_MainWindow

try:
    import linkbot_internal_dev.preassembly as preassembly
except:
    import preassembly

#import linkbot_diagnostics as diagnostics
from linkbot_diagnostics.LinkbotDiagnosticGui import initialize_tables
from linkbot_diagnostics.testlinkbot import TestLinkbot

import linkbot
import threading
import sys
import time
import traceback

class StartQT4(QtGui.QMainWindow):
    diagnostics_finished = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Linkbot Testing Suite ' + __version__)

        self.connect_preassembly_buttons()

        self.ui.pushButton_getid.clicked.connect(self.get_id)

        self.ui.pushButton_setid.setEnabled(False)
        self.ui.pushButton_setid.clicked.connect(self.set_id)
        self.ui.lineEdit_id.returnPressed.connect(self.set_id)
        self.ui.lineEdit_id.textChanged.connect(self.id_text_modified)

        self.ui.pushButton_postassembly_start.clicked.connect(
                self.start_diagnostics)
        self.diagnostics_finished.connect(self.end_diagnostics)

    def message_box(self, title, message):
        QtGui.QMessageBox.information(self, title, message)

    def preassembly_reset(self):
        try:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.groupBox_serialId.setEnabled(True)
            self.ui.groupBox_postassembly.setEnabled(True)
            self.test.exit()
            self.test = None
        except Exception as e:
            print('During preassembly reset:', e)

    def connect_preassembly_buttons(self):
        self.ui.pushButton_preassembly_reset.clicked.connect(self.preassembly_reset)
        self.ui.pushButton_preassembly_start.clicked.connect(self.preassembly_start)
        self.ui.pushButton_preassembly_next1.clicked.connect(self.preassembly_1)
        self.ui.pushButton_preassembly_next2.clicked.connect(self.preassembly_2)
        self.ui.pushButton_preassembly_next3.clicked.connect(self.preassembly_3)
        self.ui.pushButton_preassembly_next4.clicked.connect(self.preassembly_encoder)
        self.ui.pushButton_next_encoder.clicked.connect(
                self.preassembly_7)
        self.ui.pushButton_preassembly_next5.clicked.connect(self.preassembly_8)
        self.ui.pushButton_preassembly_next6.clicked.connect(self.preassembly_9)
        self.ui.pushButton_preassembly_finish.clicked.connect(self.preassembly_finish)

    def preassembly_start(self):
        try:
            self.linkbot = linkbot.Linkbot()
            self.ui.groupBox_serialId.setEnabled(False)
            self.ui.groupBox_postassembly.setEnabled(False)
            self.ui.stackedWidget.setCurrentIndex(1)
            self.test = preassembly.TestLedRed(self, linkbot=self.linkbot)
            self.test.enter()
        except Exception as e:
            self.message_box("Error", str(traceback.format_exc()))

    def preassembly_1(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.test.exit()
        self.test = preassembly.TestLedGreen(self, linkbot=self.linkbot)
        self.test.enter()

    def preassembly_2(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.test.exit()
        self.test = preassembly.TestLedBlue(self, linkbot=self.linkbot)
        self.test.enter()

    def preassembly_3(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.test.exit()
        self.test = preassembly.TestButtonPower(self, linkbot=self.linkbot)
        self.test.finished.connect(self.preassembly_4)
        self.test.enter()

    def preassembly_4(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.test.exit()
        self.test = preassembly.TestButtonA(self, linkbot=self.linkbot)
        self.test.finished.connect(self.preassembly_5)
        self.test.enter()

    def preassembly_5(self):
        self.ui.stackedWidget.setCurrentIndex(6)
        self.test.exit()
        self.test = preassembly.TestButtonB(self, linkbot=self.linkbot)
        self.test.finished.connect(self.preassembly_6)
        self.test.enter()

    def preassembly_6(self):
        self.ui.stackedWidget.setCurrentIndex(7)
        self.test.exit()
        self.test = preassembly.TestAccel(self, linkbot=self.linkbot)
        self.test.finished.connect(self.preassembly_7)
        self.test.x_changed.connect(self.ui.verticalSlider_x.setValue)
        self.test.y_changed.connect(self.ui.verticalSlider_y.setValue)
        self.test.z_changed.connect(self.ui.verticalSlider_z.setValue)
        self.test.enter()

    def preassembly_encoder(self):
        self.ui.stackedWidget.setCurrentIndex(8)
        self.test.exit()
        self.test = preassembly.TestEncoders(self, linkbot=self.linkbot)
        self.test.m1_changed.connect(self.ui.verticalSlider_1.setValue)
        self.test.m2_changed.connect(self.ui.verticalSlider_2.setValue)
        self.test.m3_changed.connect(self.ui.verticalSlider_3.setValue)
        self.test.enter()

    def preassembly_7(self):
        self.ui.stackedWidget.setCurrentIndex(9)
        self.test.exit()
        self.test = preassembly.TestMotorCcw(self, linkbot=self.linkbot)
        self.test.enter()

    def preassembly_8(self):
        self.ui.stackedWidget.setCurrentIndex(10)
        self.test.exit()
        self.test = preassembly.TestMotorCw(self, linkbot=self.linkbot)
        self.test.enter()

    def preassembly_9(self):
        self.ui.stackedWidget.setCurrentIndex(11)
        self.test.exit()
        self.test = preassembly.TestBeep(self, linkbot=self.linkbot)
        self.test.enter()
        self.ui.pushButton_beep.clicked.connect(self.test.enter)

    def preassembly_finish(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.preassembly_reset()

    def get_id(self):
        try:
            l = linkbot.Linkbot()
            self.message_box("Serial ID", l.get_serial_id())
        except:
            self.message_box("Error", str(traceback.format_exc()))

    def set_id(self):
        if len(self.ui.lineEdit_id.text()) != 4:
            self.message_box("Error", 
                    "Serial ID must be 4 characters in length.")
            return
        try:
            l = linkbot.Linkbot()
            l._setSerialId(self.ui.lineEdit_id.text().upper())
            l.set_buzzer_frequency(440)
            time.sleep(0.4)
            l.set_buzzer_frequency(0)
        except:
            self.message_box("Error", str(traceback.format_exc()))

    def id_text_modified(self, text):
        if len(text) == 4:
            self.ui.pushButton_setid.setEnabled(True)
        else:
            self.ui.pushButton_setid.setEnabled(False)

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
            linkbot = TestLinkbot('LOCL')
            x,y,z = linkbot.getAccelerometer()
            if abs(x) > 0.1 or \
               abs(x) > 0.1 or \
               abs(z-1) > 0.1:
                QtGui.QMessageBox.warning(self, 
                    "Warning",
                    "Accelerometer readings have anomalies!")
            global db_file
            con = sql.connect(db_file)
            initialize_tables(con.cursor())
            cur = con.cursor()
# Check to see if this linkbot is in our database already. Add it if not
            cur.execute('SELECT * FROM robot_type WHERE Id=\'{}\''.format(linkbot.getSerialId()))
            rows = cur.fetchall()
            formFactor = None
            if linkbot.getFormFactor() == Linkbot.FormFactor.I:
                formFactor = "Linkbot-I"
                motor2index = 2
            elif linkbot.getFormFactor() == Linkbot.FormFactor.L:
                formFactor = "Linkbot-L"
                motor2index = 1
            else:
                formFactor = "UNKNOWN"
            print ("Testing LinkBot {}".format(linkbot.getSerialId()))
            d = LinkbotDiagnostic(linkbot)
            results = d.runLinearityTest()
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            if len(rows) == 0:
                cur.execute('INSERT INTO robot_type VALUES(\'{}\', \'{}\')'.format(
                    linkbot.getSerialId(), formFactor))
            cur.execute("INSERT INTO linearity_tests "
                "VALUES('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(
                    linkbot.getSerialId(),
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
            self.ui.m1f.setText(str(results[0]['forward_slope']))
            self.ui.m1fl.setText(str(results[0]['forward_rvalue']))
            self.ui.m1b.setText(str(results[0]['backward_slope']))
            self.ui.m1bl.setText(str(results[0]['backward_rvalue']))

            self.ui.m2f.setText(str(results[motor2index]['forward_slope']))
            self.ui.m2fl.setText(str(results[motor2index]['forward_rvalue']))
            self.ui.m2b.setText(str(results[motor2index]['backward_slope']))
            self.ui.m2bl.setText(str(results[motor2index]['backward_rvalue']))
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
            QtGui.QMessageBox.warning(self, 
                    "Warning",
                    "Test Failed: " + str(e))
            self.diagnostics_finished.emit(0)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
