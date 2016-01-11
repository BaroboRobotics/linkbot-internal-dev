# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final.ui'
#
# Created: Fri Jan  8 15:06:50 2016
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(344, 252)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_m1fs = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_m1fs.setObjectName(_fromUtf8("lineEdit_m1fs"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_m1fs)
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_m1fl = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_m1fl.setObjectName(_fromUtf8("lineEdit_m1fl"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_m1fl)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_m1bs = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_m1bs.setObjectName(_fromUtf8("lineEdit_m1bs"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_m1bs)
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_m1bl = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_m1bl.setObjectName(_fromUtf8("lineEdit_m1bl"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_m1bl)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_5)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_5 = QtGui.QLabel(self.groupBox_5)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_m2fs = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_m2fs.setObjectName(_fromUtf8("lineEdit_m2fs"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_m2fs)
        self.label_6 = QtGui.QLabel(self.groupBox_5)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_m2fl = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_m2fl.setObjectName(_fromUtf8("lineEdit_m2fl"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_m2fl)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.formLayout_4 = QtGui.QFormLayout(self.groupBox_6)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_7 = QtGui.QLabel(self.groupBox_6)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_m2bs = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_m2bs.setObjectName(_fromUtf8("lineEdit_m2bs"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_m2bs)
        self.label_8 = QtGui.QLabel(self.groupBox_6)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lineEdit_m2bl = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_m2bl.setObjectName(_fromUtf8("lineEdit_m2bl"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_m2bl)
        self.verticalLayout_2.addWidget(self.groupBox_6)
        self.horizontalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Motor 1", None))
        self.groupBox_3.setTitle(_translate("Form", "Positive Dir", None))
        self.label.setText(_translate("Form", "Speed", None))
        self.label_2.setText(_translate("Form", "Lin.", None))
        self.groupBox_4.setTitle(_translate("Form", "Negative Dir", None))
        self.label_3.setText(_translate("Form", "Speed", None))
        self.label_4.setText(_translate("Form", "Lin.", None))
        self.groupBox_2.setTitle(_translate("Form", "Motor 2/3", None))
        self.groupBox_5.setTitle(_translate("Form", "Positive Dir", None))
        self.label_5.setText(_translate("Form", "Speed", None))
        self.label_6.setText(_translate("Form", "Lin.", None))
        self.groupBox_6.setTitle(_translate("Form", "Negative Dir", None))
        self.label_7.setText(_translate("Form", "Speed", None))
        self.label_8.setText(_translate("Form", "Lin.", None))

