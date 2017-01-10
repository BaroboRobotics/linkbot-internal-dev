#!/usr/bin/env python3

__version__ = "1.2.2"

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

import threading
import sys
import time
import traceback
import os

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
                       (tests.ButtonPwr, None),
                       (tests.ButtonA, None),
                       (tests.ButtonB, self.ui.checkBox_button),
                       (tests.Buzzer, self.ui.checkBox_buzzer),
                       (tests.LedRed, None),
                       (tests.LedGreen, None),
                       (tests.LedBlue, self.ui.checkBox_led),
                       (tests.AccelerometerZ, None),
                       (tests.AccelerometerY, None),
                       (tests.AccelerometerX, self.ui.checkBox_accelerometer),
                       (tests.Calibration, self.ui.checkBox_calibration),
                       (tests.Radio, self.ui.checkBox_radio),
                       (tests.MotorTest, self.ui.checkBox_motor_test),
                       (tests.Final, None),
                     ]

        self.dongle_tests = [ 
                       (tests.Radio, self.ui.checkBox_radio),
                       (tests.FinalDongle, None),
                            ]

        self._test_state = {}

        self.reset_ui()

        self.ui.pushButton_restart.clicked.connect(self.reset_ui)
        
    def display_next_test(self):
        try:
            if self._test[1] is not None:
                self._test[1].setChecked(True)
        except Exception as e:
            print('While trying to set checkbox:', e)

        if self._test_widget is not None:
            try:
                self._test_widget.deinit()
            except:
                pass
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

        self._test_widget = self._test[0](self, state=self._test_state)
        self._test_widget.completed.connect(self.display_next_test)
        self._test_widget.failure.connect(self.failure)
        self._test_widget.show()

        self.ui.test_content_layout.addWidget(self._test_widget)

        self._test_widget.run()

    def failure(self, msg):
        self.clear_ui()
        # Load a failure label
        try:
            self._test_widget = tests.Failure(self, state=self._test_state, msg=msg)
            self._test_widget.show()
            self.ui.test_content_layout.addWidget(self._test_widget)
            self._test_widget.completed.connect(self.reset_ui)
            self._test_widget.run()
        except Exception as e:
            print(traceback.format_exc())
            return

    def reset_ui(self):
        self.clear_ui()
        for b in self.checkboxes:
            b.setChecked(False)

        self._tests = iter(self.tests)
        self._test = None
        self._test_widget = None

        self.display_next_test()

    def clear_ui(self):
        # Clear the content area
        try:
            self._test_widget.deinit()
        except Exception as e:
            print('Exception occured during deinit:', traceback.format_exc())
        try:
            self.ui.test_content_layout.removeWidget(self._test_widget)
            self._test_widget.hide()
            del self._test_widget
        except Exception as e:
            print(traceback.format_exc())
            return

    def message_box(self, title, message):
        QtGui.QMessageBox.information(self, title, message)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    app.aboutToQuit.connect(myapp.clear_ui)
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
