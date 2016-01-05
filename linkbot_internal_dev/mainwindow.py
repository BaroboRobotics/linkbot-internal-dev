# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Jan  4 16:44:53 2016
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
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setCheckable(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setCheckable(False)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setCheckable(False)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.verticalLayout.addWidget(self.checkBox_3)
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_4.setCheckable(False)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.verticalLayout.addWidget(self.checkBox_4)
        self.checkBox_5 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_5.setCheckable(False)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.verticalLayout.addWidget(self.checkBox_5)
        self.checkBox_6 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_6.setCheckable(False)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.verticalLayout.addWidget(self.checkBox_6)
        self.checkBox_7 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_7.setCheckable(False)
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.verticalLayout.addWidget(self.checkBox_7)
        self.checkBox_8 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_8.setCheckable(False)
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        self.verticalLayout.addWidget(self.checkBox_8)
        self.checkBox_9 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_9.setCheckable(False)
        self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))
        self.verticalLayout.addWidget(self.checkBox_9)
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
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_2.addWidget(self.pushButton)
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
        self.checkBox.setText(_translate("MainWindow", "Linkbot Detected", None))
        self.checkBox_2.setText(_translate("MainWindow", "Serial ID Programmed", None))
        self.checkBox_3.setText(_translate("MainWindow", "Radio Test", None))
        self.checkBox_4.setText(_translate("MainWindow", "Button Test", None))
        self.checkBox_5.setText(_translate("MainWindow", "Buzzer Test", None))
        self.checkBox_6.setText(_translate("MainWindow", "LED Color Test", None))
        self.checkBox_7.setText(_translate("MainWindow", "Accelerometer Test", None))
        self.checkBox_8.setText(_translate("MainWindow", "Calibration", None))
        self.checkBox_9.setText(_translate("MainWindow", "Motor Test", None))
        self.groupBox_test_content.setTitle(_translate("MainWindow", "Test Instructions", None))
        self.pushButton.setText(_translate("MainWindow", "Restart", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

