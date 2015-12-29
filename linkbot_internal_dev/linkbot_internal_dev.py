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

import linkbot
import sys
import time

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Linkbot Testing Suite ' + __version__)

        self.connect_preassembly_buttons()

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
        self.ui.pushButton_preassembly_next4.clicked.connect(self.preassembly_7)
        self.ui.pushButton_preassembly_next5.clicked.connect(self.preassembly_8)
        self.ui.pushButton_preassembly_next6.clicked.connect(self.preassembly_9)
        self.ui.pushButton_preassembly_finish.clicked.connect(self.preassembly_finish)

    def preassembly_start(self):
        self.ui.groupBox_serialId.setEnabled(False)
        self.ui.groupBox_postassembly.setEnabled(False)
        self.ui.stackedWidget.setCurrentIndex(1)
        self.linkbot = linkbot.Linkbot()
        self.test = preassembly.TestLedRed(self, linkbot=self.linkbot)
        self.test.enter()

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

    def preassembly_7(self):
        self.ui.stackedWidget.setCurrentIndex(8)
        self.test.exit()
        self.test = preassembly.TestMotorCcw(self, linkbot=self.linkbot)
        self.test.enter()

    def preassembly_8(self):
        self.ui.stackedWidget.setCurrentIndex(9)
        self.test.exit()
        self.test = preassembly.TestMotorCw(self, linkbot=self.linkbot)
        self.test.enter()

    def preassembly_9(self):
        self.ui.stackedWidget.setCurrentIndex(10)
        self.test.exit()
        self.test = preassembly.TestBeep(self, linkbot=self.linkbot)
        self.test.enter()
        self.ui.pushButton_beep.clicked.connect(self.test.enter)

    def preassembly_finish(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.preassembly_reset()

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
