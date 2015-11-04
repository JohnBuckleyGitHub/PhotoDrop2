import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import ctypes
import io
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
        # self.transfer_table = PhotoDropFunctions.pd_ui_class(self, "transfer")

        self.show()
        self.signalMapper = QtCore.QSignalMapper(self)

        self.in_dir_tableWidget.cellDoubleClicked.connect(self.tables.input_table.load_picture)
        self.browse_input_pushButton.clicked.connect(self.tables.input_table.browse_directory)
        self.refresh_input_pushButton.clicked.connect(self.tables.input_table.refresh_table)
        self.transfer_input_trans_pushButton.clicked.connect(self.tables.input_transfer_selection)

        self.in_dir_tableWidget.itemDropped.connect(self.tables.input_table.append_from_event)
        self.in_dir_tableWidget.itemUrlPasted.connect(self.tables.input_table.append_from_event)
        self.in_dir_tableWidget.itemImagePasted.connect(self.tables.input_table.save_image_from_paste)
        self.in_dir_tableWidget.itemImageDelete.connect(self.tables.input_table.delete_selection)

        self.transfer_tableWidget.itemDropped.connect(self.tables.transfer_table.append_from_event)
        self.transfer_tableWidget.itemUrlPasted.connect(self.tables.transfer_table.append_from_event)
        self.transfer_tableWidget.itemImagePasted.connect(self.tables.image_paste_into_transfer)
        self.transfer_tableWidget.itemImageDelete.connect(self.tables.transfer_table.delete_selection)




if __name__ == '__main__':
    myappid = 'Photinput_tableoDrop.Beta.0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = MyWindow()
    sys.exit(app.exec_())
