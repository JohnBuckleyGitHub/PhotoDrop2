# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Johns Lenovo\Documents\Python Projects\py2exe_builds\PhotoDrop\PhotoDrop.ui'
#
# Created: Mon Dec 14 17:47:46 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1460, 1045)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.output_sort_comboBox = QtGui.QComboBox(self.centralwidget)
        self.output_sort_comboBox.setObjectName(_fromUtf8("output_sort_comboBox"))
        self.gridLayout.addWidget(self.output_sort_comboBox, 3, 10, 1, 2)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 3, 9, 1, 1)
        self.transfer_tableWidget = TableWithPaste(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transfer_tableWidget.sizePolicy().hasHeightForWidth())
        self.transfer_tableWidget.setSizePolicy(sizePolicy)
        self.transfer_tableWidget.setMinimumSize(QtCore.QSize(300, 700))
        self.transfer_tableWidget.setObjectName(_fromUtf8("transfer_tableWidget"))
        self.transfer_tableWidget.setColumnCount(0)
        self.transfer_tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.transfer_tableWidget, 4, 5, 7, 3)
        self.output_directory_tableWidget = TableWithPaste(self.centralwidget)
        self.output_directory_tableWidget.setMinimumSize(QtCore.QSize(300, 700))
        self.output_directory_tableWidget.setObjectName(_fromUtf8("output_directory_tableWidget"))
        self.output_directory_tableWidget.setColumnCount(0)
        self.output_directory_tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.output_directory_tableWidget, 4, 9, 7, 3)
        self.pd_untransfer_input_trans_pushButton = QtGui.QPushButton(self.centralwidget)
        self.pd_untransfer_input_trans_pushButton.setObjectName(_fromUtf8("pd_untransfer_input_trans_pushButton"))
        self.gridLayout.addWidget(self.pd_untransfer_input_trans_pushButton, 6, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(12, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 12, 1, 1)
        self.pd_untransfer_output_trans_pushButton = QtGui.QPushButton(self.centralwidget)
        self.pd_untransfer_output_trans_pushButton.setObjectName(_fromUtf8("pd_untransfer_output_trans_pushButton"))
        self.gridLayout.addWidget(self.pd_untransfer_output_trans_pushButton, 6, 8, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 8, 1, 1)
        self.input_sort_comboBox = QtGui.QComboBox(self.centralwidget)
        self.input_sort_comboBox.setObjectName(_fromUtf8("input_sort_comboBox"))
        self.gridLayout.addWidget(self.input_sort_comboBox, 3, 2, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.input_directory_tableWidget = TableWithPaste(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_directory_tableWidget.sizePolicy().hasHeightForWidth())
        self.input_directory_tableWidget.setSizePolicy(sizePolicy)
        self.input_directory_tableWidget.setMinimumSize(QtCore.QSize(300, 700))
        self.input_directory_tableWidget.setObjectName(_fromUtf8("input_directory_tableWidget"))
        self.input_directory_tableWidget.setColumnCount(0)
        self.input_directory_tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.input_directory_tableWidget, 4, 1, 7, 3)
        self.pd_transfer_input_trans_pushButton = QtGui.QPushButton(self.centralwidget)
        self.pd_transfer_input_trans_pushButton.setObjectName(_fromUtf8("pd_transfer_input_trans_pushButton"))
        self.gridLayout.addWidget(self.pd_transfer_input_trans_pushButton, 5, 4, 1, 1)
        self.pd_transfer_output_trans_pushButton = QtGui.QPushButton(self.centralwidget)
        self.pd_transfer_output_trans_pushButton.setObjectName(_fromUtf8("pd_transfer_output_trans_pushButton"))
        self.gridLayout.addWidget(self.pd_transfer_output_trans_pushButton, 5, 8, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 4, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 1, 1, 1)
        self.pd_increment_letter_lineEdit = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pd_increment_letter_lineEdit.sizePolicy().hasHeightForWidth())
        self.pd_increment_letter_lineEdit.setSizePolicy(sizePolicy)
        self.pd_increment_letter_lineEdit.setObjectName(_fromUtf8("pd_increment_letter_lineEdit"))
        self.gridLayout.addWidget(self.pd_increment_letter_lineEdit, 3, 7, 1, 1)
        self.pd_prefix_lineEdit = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pd_prefix_lineEdit.sizePolicy().hasHeightForWidth())
        self.pd_prefix_lineEdit.setSizePolicy(sizePolicy)
        self.pd_prefix_lineEdit.setObjectName(_fromUtf8("pd_prefix_lineEdit"))
        self.gridLayout.addWidget(self.pd_prefix_lineEdit, 3, 5, 1, 1)
        self.pd_run_number_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.pd_run_number_spinBox.setMaximum(99999)
        self.pd_run_number_spinBox.setObjectName(_fromUtf8("pd_run_number_spinBox"))
        self.gridLayout.addWidget(self.pd_run_number_spinBox, 3, 6, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 6, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 5, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 7, 1, 1)
        self.transfer_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.transfer_checkBox.setObjectName(_fromUtf8("transfer_checkBox"))
        self.gridLayout.addWidget(self.transfer_checkBox, 1, 7, 1, 1)
        self.pd_last_run_pushButton = QtGui.QPushButton(self.centralwidget)
        self.pd_last_run_pushButton.setObjectName(_fromUtf8("pd_last_run_pushButton"))
        self.gridLayout.addWidget(self.pd_last_run_pushButton, 1, 6, 1, 1)
        self.pd_database_settings_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pd_database_settings_pushButton.sizePolicy().hasHeightForWidth())
        self.pd_database_settings_pushButton.setSizePolicy(sizePolicy)
        self.pd_database_settings_pushButton.setObjectName(_fromUtf8("pd_database_settings_pushButton"))
        self.gridLayout.addWidget(self.pd_database_settings_pushButton, 1, 5, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.input_directory_comboBox = QtGui.QComboBox(self.centralwidget)
        self.input_directory_comboBox.setObjectName(_fromUtf8("input_directory_comboBox"))
        self.gridLayout.addWidget(self.input_directory_comboBox, 2, 2, 1, 2)
        self.input_refresh_pushButton = QtGui.QPushButton(self.centralwidget)
        self.input_refresh_pushButton.setObjectName(_fromUtf8("input_refresh_pushButton"))
        self.gridLayout.addWidget(self.input_refresh_pushButton, 1, 1, 1, 1)
        self.input_browse_pushButton = QtGui.QPushButton(self.centralwidget)
        self.input_browse_pushButton.setObjectName(_fromUtf8("input_browse_pushButton"))
        self.gridLayout.addWidget(self.input_browse_pushButton, 1, 2, 1, 1)
        self.input_picture_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.input_picture_checkBox.setObjectName(_fromUtf8("input_picture_checkBox"))
        self.gridLayout.addWidget(self.input_picture_checkBox, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 9, 1, 1)
        self.output_directory_comboBox = QtGui.QComboBox(self.centralwidget)
        self.output_directory_comboBox.setObjectName(_fromUtf8("output_directory_comboBox"))
        self.gridLayout.addWidget(self.output_directory_comboBox, 2, 10, 1, 2)
        self.output_picture_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.output_picture_checkBox.setObjectName(_fromUtf8("output_picture_checkBox"))
        self.gridLayout.addWidget(self.output_picture_checkBox, 1, 11, 1, 1)
        self.output_browse_pushButton = QtGui.QPushButton(self.centralwidget)
        self.output_browse_pushButton.setObjectName(_fromUtf8("output_browse_pushButton"))
        self.gridLayout.addWidget(self.output_browse_pushButton, 1, 10, 1, 1)
        self.output_refresh_pushButton = QtGui.QPushButton(self.centralwidget)
        self.output_refresh_pushButton.setObjectName(_fromUtf8("output_refresh_pushButton"))
        self.gridLayout.addWidget(self.output_refresh_pushButton, 1, 9, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1460, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_7.setText(_translate("MainWindow", "Sort Scheme", None))
        self.pd_untransfer_input_trans_pushButton.setText(_translate("MainWindow", "<<<", None))
        self.pd_untransfer_output_trans_pushButton.setText(_translate("MainWindow", "<<<", None))
        self.pd_transfer_input_trans_pushButton.setText(_translate("MainWindow", ">>>", None))
        self.pd_transfer_output_trans_pushButton.setText(_translate("MainWindow", ">>>", None))
        self.label_6.setText(_translate("MainWindow", "Sort Scheme", None))
        self.label_5.setText(_translate("MainWindow", "Run Number", None))
        self.label_3.setText(_translate("MainWindow", "Prefix", None))
        self.label_4.setText(_translate("MainWindow", "Increment Letter", None))
        self.transfer_checkBox.setText(_translate("MainWindow", "Load Pictures", None))
        self.pd_last_run_pushButton.setText(_translate("MainWindow", "Last Run", None))
        self.pd_database_settings_pushButton.setText(_translate("MainWindow", "Run DB Settings", None))
        self.label.setText(_translate("MainWindow", "Input Directory", None))
        self.input_refresh_pushButton.setText(_translate("MainWindow", "Refresh Table", None))
        self.input_browse_pushButton.setText(_translate("MainWindow", "Browse Input Directory", None))
        self.input_picture_checkBox.setText(_translate("MainWindow", "Load Pictures", None))
        self.label_2.setText(_translate("MainWindow", "Storage Directory", None))
        self.output_picture_checkBox.setText(_translate("MainWindow", "Load Pictures", None))
        self.output_browse_pushButton.setText(_translate("MainWindow", "Browse Output Directory", None))
        self.output_refresh_pushButton.setText(_translate("MainWindow", "Refresh Table", None))

from table_with_paste import TableWithPaste
