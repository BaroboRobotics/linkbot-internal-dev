# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Jan  6 15:26:31 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 380)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_serial_id = QtGui.QCheckBox(self.groupBox)
        self.checkBox_serial_id.setCheckable(True)
        self.checkBox_serial_id.setObjectName(_fromUtf8("checkBox_serial_id"))
        self.verticalLayout.addWidget(self.checkBox_serial_id)
        self.checkBox_button = QtGui.QCheckBox(self.groupBox)
        self.checkBox_button.setCheckable(True)
        self.checkBox_button.setObjectName(_fromUtf8("checkBox_button"))
        self.verticalLayout.addWidget(self.checkBox_button)
        self.checkBox_buzzer = QtGui.QCheckBox(self.groupBox)
        self.checkBox_buzzer.setCheckable(True)
        self.checkBox_buzzer.setObjectName(_fromUtf8("checkBox_buzzer"))
        self.verticalLayout.addWidget(self.checkBox_buzzer)
        self.checkBox_led = QtGui.QCheckBox(self.groupBox)
        self.checkBox_led.setCheckable(True)
        self.checkBox_led.setObjectName(_fromUtf8("checkBox_led"))
        self.verticalLayout.addWidget(self.checkBox_led)
        self.checkBox_accelerometer = QtGui.QCheckBox(self.groupBox)
        self.checkBox_accelerometer.setCheckable(True)
        self.checkBox_accelerometer.setObjectName(_fromUtf8("checkBox_accelerometer"))
        self.verticalLayout.addWidget(self.checkBox_accelerometer)
        self.checkBox_calibration = QtGui.QCheckBox(self.groupBox)
        self.checkBox_calibration.setCheckable(True)
        self.checkBox_calibration.setObjectName(_fromUtf8("checkBox_calibration"))
        self.verticalLayout.addWidget(self.checkBox_calibration)
        self.checkBox_radio = QtGui.QCheckBox(self.groupBox)
        self.checkBox_radio.setCheckable(True)
        self.checkBox_radio.setObjectName(_fromUtf8("checkBox_radio"))
        self.verticalLayout.addWidget(self.checkBox_radio)
        self.checkBox_motor_test = QtGui.QCheckBox(self.groupBox)
        self.checkBox_motor_test.setCheckable(True)
        self.checkBox_motor_test.setObjectName(_fromUtf8("checkBox_motor_test"))
        self.verticalLayout.addWidget(self.checkBox_motor_test)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_test_content = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_test_content.sizePolicy().hasHeightForWidth())
        self.groupBox_test_content.setSizePolicy(sizePolicy)
        self.groupBox_test_content.setObjectName(_fromUtf8("groupBox_test_content"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_test_content)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.test_content_layout = QtGui.QVBoxLayout()
        self.test_content_layout.setObjectName(_fromUtf8("test_content_layout"))
        self.verticalLayout_4.addLayout(self.test_content_layout)
        self.verticalLayout_2.addWidget(self.groupBox_test_content)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.pushButton_restart = QtGui.QPushButton(self.centralwidget)
        self.pushButton_restart.setObjectName(_fromUtf8("pushButton_restart"))
        self.verticalLayout_2.addWidget(self.pushButton_restart)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Checklist", None))
        self.checkBox_serial_id.setText(_translate("MainWindow", "Serial ID Programmed", None))
        self.checkBox_button.setText(_translate("MainWindow", "Button Test", None))
        self.checkBox_buzzer.setText(_translate("MainWindow", "Buzzer Test", None))
        self.checkBox_led.setText(_translate("MainWindow", "LED Color Test", None))
        self.checkBox_accelerometer.setText(_translate("MainWindow", "Accelerometer Test", None))
        self.checkBox_calibration.setText(_translate("MainWindow", "Calibration", None))
        self.checkBox_radio.setText(_translate("MainWindow", "Radio Test", None))
        self.checkBox_motor_test.setText(_translate("MainWindow", "Motor Test", None))
        self.groupBox_test_content.setTitle(_translate("MainWindow", "Test Instructions", None))
        self.pushButton_restart.setText(_translate("MainWindow", "Restart", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

