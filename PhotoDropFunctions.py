import PictureDirTable


class pd_ui_class(PictureDirTable.Pic_Dir_Table):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.input_table()
        self.transfer_table()

    def input_table(self):
        self.input_table = PictureDirTable.Pic_Dir_Table()
        self.input_table.directory_lineEdit = self.parent.input_directory_lineEdit
        self.input_table.directory_lineEdit.setText('C:/Users/Johns Lenovo/Pictures')
        self.input_table.table = self.parent.in_dir_tableWidget
        self.input_table.create_dir_table_data()
        self.input_table.table_from_list()

    def transfer_table(self):
        self.transfer_table = PictureDirTable.Pic_Dir_Table()
        self.transfer_table.table = self.parent.transfer_tableWidget
        self.transfer_table.create_empty_table()

    def input_transfer_selection(self):
        transfer_list = self.input_table.transfer_selection()
        self.transfer_table.add_selections(transfer_list)
        self.transfer_table.table_from_list()
