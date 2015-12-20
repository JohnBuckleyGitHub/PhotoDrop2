# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Johns Lenovo\Documents\Python Projects\py2exe_builds\PhotoDrop\DBWindow.ui'
#
# Created: Mon Dec 14 17:49:12 2015
#      by: PyQt4 UI code generator 4.11.3
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
        Form.resize(1431, 738)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.use_db_checkBox = QtGui.QCheckBox(Form)
        self.use_db_checkBox.setObjectName(_fromUtf8("use_db_checkBox"))
        self.gridLayout.addWidget(self.use_db_checkBox, 0, 0, 1, 1)
        self.db_info_groupBox = QtGui.QGroupBox(Form)
        self.db_info_groupBox.setTitle(_fromUtf8(""))
        self.db_info_groupBox.setObjectName(_fromUtf8("db_info_groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.db_info_groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.uid_groupBox = QtGui.QGroupBox(self.db_info_groupBox)
        self.uid_groupBox.setTitle(_fromUtf8(""))
        self.uid_groupBox.setObjectName(_fromUtf8("uid_groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.uid_groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_3 = QtGui.QLabel(self.uid_groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.login_comboBox = QtGui.QComboBox(self.uid_groupBox)
        self.login_comboBox.setEditable(True)
        self.login_comboBox.setObjectName(_fromUtf8("login_comboBox"))
        self.gridLayout_2.addWidget(self.login_comboBox, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.uid_groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.password_comboBox = QtGui.QComboBox(self.uid_groupBox)
        self.password_comboBox.setEditable(True)
        self.password_comboBox.setObjectName(_fromUtf8("password_comboBox"))
        self.gridLayout_2.addWidget(self.password_comboBox, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.uid_groupBox, 2, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.db_info_groupBox)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.server_name_comboBox = QtGui.QComboBox(self.groupBox_3)
        self.server_name_comboBox.setEditable(True)
        self.server_name_comboBox.setObjectName(_fromUtf8("server_name_comboBox"))
        self.gridLayout_3.addWidget(self.server_name_comboBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.db_name_comboBox = QtGui.QComboBox(self.groupBox_3)
        self.db_name_comboBox.setEditable(True)
        self.db_name_comboBox.setObjectName(_fromUtf8("db_name_comboBox"))
        self.gridLayout_3.addWidget(self.db_name_comboBox, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.windows_auth_checkBox = QtGui.QCheckBox(self.db_info_groupBox)
        self.windows_auth_checkBox.setObjectName(_fromUtf8("windows_auth_checkBox"))
        self.gridLayout_4.addWidget(self.windows_auth_checkBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.db_info_groupBox, 1, 0, 1, 2)
        self.ok_pushButton = QtGui.QPushButton(Form)
        self.ok_pushButton.setObjectName(_fromUtf8("ok_pushButton"))
        self.gridLayout.addWidget(self.ok_pushButton, 2, 0, 1, 1)
        self.cancel_pushButton = QtGui.QPushButton(Form)
        self.cancel_pushButton.setObjectName(_fromUtf8("cancel_pushButton"))
        self.gridLayout.addWidget(self.cancel_pushButton, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.use_db_checkBox.setText(_translate("Form", "Use database information", None))
        self.label_3.setText(_translate("Form", "Login", None))
        self.label_4.setText(_translate("Form", "Password", None))
        self.label_2.setText(_translate("Form", "Database name", None))
        self.label.setText(_translate("Form", "Server name", None))
        self.windows_auth_checkBox.setText(_translate("Form", "Use Windows Authentication", None))
        self.ok_pushButton.setText(_translate("Form", "Ok", None))
        self.cancel_pushButton.setText(_translate("Form", "Cancel", None))

