from PyQt4 import QtGui
from PyQt4 import QtCore
import PictureDirTable


class pd_ui_class(PictureDirTable.Pic_Dir_Table):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.input_table()
        self.transfer_table()

    def input_table(self):
        self.input_table = PictureDirTable.Pic_Dir_Table(self.parent)
        # self.input_table.parent = self.parent
        self.input_table.directory_lineEdit = self.parent.input_directory_lineEdit
        self.input_table.directory_lineEdit.setText('C:/Users/Johns Lenovo/Pictures')
        self.input_table.table = self.parent.in_dir_tableWidget
        self.input_table.create_dir_table_data()
        self.input_table.table_from_list()

    def transfer_table(self):
        self.transfer_table = PictureDirTable.Pic_Dir_Table(self.parent)
        # self.transfer_table.parent = self.parent
        self.transfer_table.table = self.parent.transfer_tableWidget
        self.transfer_table.create_empty_table()

    def input_transfer_selection(self):
        transfer_list = self.input_table.transfer_selection()
        self.transfer_table.add_selections(transfer_list)
        self.transfer_table.table_from_list()
        self.input_table.table_from_list()

    def input_untransfer_selection(self):
        transfer_list = self.transfer_table.transfer_selection()
        self.input_table.add_selections(transfer_list)
        self.transfer_table.table_from_list()
        self.input_table.table_from_list()

    def image_paste_into_transfer(self, mime_data):
        self.parent.in_dir_tableWidget.itemImagePasted.emit(mime_data)
        last_row = self.parent.in_dir_tableWidget.rowCount() - 1
        for col in range(self.parent.in_dir_tableWidget.columnCount()):
            self.parent.in_dir_tableWidget.item(last_row, col).setSelected(True)
        self.input_transfer_selection()

    def select_first_row(self):
        self.my_tableWidget
