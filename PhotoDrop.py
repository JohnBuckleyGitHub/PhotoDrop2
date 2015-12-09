import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import ctypes
sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets
import PhotoDropFunctions


class MyWindow(QtGui.QMainWindow, kustomWidgets.status_label_class):  # PhotoDropFunctions.pic_dir_table

    def __init__(self):
        super().__init__()
        uic.loadUi('PhotoDrop.ui', self)
        self.setWindowTitle('Photo Renamer')
        self.brush = kustomWidgets.brushstyle()
        self.tables = PhotoDropFunctions.pd_ui_class(self)
        self.thread_pool = QtCore.QThreadPool()

        self.show()
        self.signalMapper = QtCore.QSignalMapper(self)

        self.in_dir_tableWidget.cellDoubleClicked.connect(self.tables.input_table.load_picture)
        self.browse_input_pushButton.clicked.connect(self.tables.input_table.browse_directory)
        self.refresh_input_pushButton.clicked.connect(self.tables.input_table.refresh_table)
        self.transfer_input_trans_pushButton.clicked.connect(self.tables.input_transfer_selection)
        self.untransfer_input_trans_pushButton.clicked.connect(self.tables.input_untransfer_selection)

        self.in_dir_tableWidget.itemDropped.connect(self.tables.input_table.append_from_event)
        self.in_dir_tableWidget.itemUrlPasted.connect(self.tables.input_table.append_from_event)
        self.in_dir_tableWidget.itemImageScaled.connect(self.tables.load_item)
        self.in_dir_tableWidget.itemImagePasted.connect(self.tables.input_table.save_image_from_paste)
        self.in_dir_tableWidget.itemImageDelete.connect(self.tables.input_table.delete_selection)
        self.input_checkBox.clicked.connect(self.tables.input_table.table_from_list)
        # self.comboBox.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        # self.comboBox.setEditable(True)
        # self.comboBox.activated.connect(self.print_comboBox)

        self.transfer_tableWidget.itemDropped.connect(self.tables.transfer_table.append_from_event)
        self.transfer_tableWidget.itemUrlPasted.connect(self.tables.transfer_table.append_from_event)
        self.transfer_tableWidget.itemImagePasted.connect(self.tables.image_paste_into_transfer)
        self.transfer_tableWidget.itemImageDelete.connect(self.tables.input_untransfer_selection)
        self.transfer_checkBox.clicked.connect(self.tables.transfer_table.table_from_list)

        self.out_dir_tableWidget.cellDoubleClicked.connect(self.tables.output_table.load_picture)
        self.browse_output_pushButton.clicked.connect(self.tables.output_table.browse_directory)
        self.refresh_output_pushButton.clicked.connect(self.tables.output_table.refresh_table)
        self.transfer_output_trans_pushButton.clicked.connect(self.tables.output_transfer_selection)
        self.untransfer_output_trans_pushButton.clicked.connect(self.tables.output_untransfer_selection)

        self.output_checkBox.clicked.connect(self.tables.output_table.table_from_list)




if __name__ == '__main__':
    myappid = 'Photinput_tableoDrop.Beta.0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = MyWindow()
    sys.exit(app.exec_())
