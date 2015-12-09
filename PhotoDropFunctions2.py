import shutil
from send2trash import send2trash


class pd_ui_class(PictureDirTable.Pic_Dir_Table):

    signal1 = QtCore.SIGNAL("test signal")  # test code
class pd_ui_class(QtCore.QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # super().__init__()
        self.input_table()
        self.transfer_table()
        self.output_table()

    def input_table(self):
        self.input_table = PictureDirTable.Pic_Dir_Table(self.parent)
        self.input_table.checkbox = self.parent.input_checkBox
        # self.input_table.parent = self.parent
        # self.input_table.directory_lineEdit = self.parent.input_directory_lineEdit
        # self.input_table.input_director_comboBox.setText('C:/Users/Johns Lenovo/Documents/Pictures/I15C07 SW SOS')
        self.input_table.directory_comboBox = self.parent.input_directory_comboBox
        ui_dict = {'table': 'in_dir_tableWidget',
                   'browse_button': 'browse_input_pushButton',
                   'refresh_button': 'refresh_input_pushButton',
                   'checkbox': 'input_checkBox',
                   'directory_comboBox': 'input_directory_comboBox'}
        self.input_table = PictureDirTable.Pic_Dir_Table('input_table')
        self.input_table.setup_connects(self.parent, ui_dict)
        # self.input_table.directory_comboBox = self.parent.input_directory_comboBox
        directory_list = ['C:/Users/Johns Lenovo/Documents/Pictures/I15C07 SW SOS',
                          'C:\\PME_Mirror\\GM_IndyCar\\Vehicle_Data\\Aero\\WT\\PTG\\PME\\15C07\\Photos']
        self.input_table.directory_comboBox.insertItems(0, directory_list)
        self.input_table.table = self.parent.in_dir_tableWidget
        # self.input_table.table = self.parent.in_dir_tableWidget
        self.input_table.create_dir_table_data()
        self.input_table.table_from_list()
        self.input_table.directory_comboBox.currentIndexChanged.connect(self.input_table.refresh_table)

    def load_item(self, input_object):
        row, image = input_object
@@ -41,23 +42,35 @@ class pd_ui_class(PictureDirTable.Pic_Dir_Table):
        self.input_table.table.setItem(row, 1, item)

    def transfer_table(self):
        self.transfer_table = PictureDirTable.Pic_Dir_Table(self.parent)
        self.transfer_table.checkbox = self.parent.transfer_checkBox
        ui_dict = {'table': 'transfer_tableWidget',
                   'browse_button': 'browse_input_pushButton',
                   'refresh_button': 'refresh_input_pushButton',
                   'checkbox': 'input_checkBox',
                   'directory_comboBox': 'input_directory_comboBox'}
        self.transfer_table = PictureDirTable.Pic_Dir_Table('transfer_table')  # self.parent)
        self.transfer_table.setup_connects(self.parent, ui_dict)
        # self.transfer_table.checkbox = self.parent.transfer_checkBox
        # self.transfer_table.parent = self.parent
        self.transfer_table.table = self.parent.transfer_tableWidget
        self.transfer_table.create_empty_table()
        # self.transfer_table.table = self.parent.transfer_tableWidget
        self.transfer_table.pics_in_dir = []

    def output_table(self):
        self.output_table = PictureDirTable.Pic_Dir_Table(self.parent)
        self.output_table.checkbox = self.parent.output_checkBox
        ui_dict = {'table': 'out_dir_tableWidget',
                   'browse_button': 'browse_output_pushButton',
                   'refresh_button': 'refresh_output_pushButton',
                   'checkbox': 'output_checkBox',
                   'directory_comboBox': 'output_directory_comboBox'}
        self.output_table = PictureDirTable.Pic_Dir_Table('output_table')  # self.parent)
        # self.output_table.checkbox = self.parent.output_checkBox
        # self.transfer_table.parent = self.parent
        # self.output_table.directory_lineEdit = self.parent.output_directory_lineEdit
        # self.output_table.directory_lineEdit.setText('C:/Users/Johns Lenovo/Documents/Pictures')
        self.output_table.directory_comboBox = self.parent.output_directory_comboBox
        # self.output_table.directory_comboBox = self.parent.output_directory_comboBox
        self.output_table.setup_connects(self.parent, ui_dict)
        directory_list = ['C:/Users/Johns Lenovo/Documents/Pictures/I15C07 SW SOS',
                          'C:\\PME_Mirror\\GM_IndyCar\\Vehicle_Data\\Aero\\WT\\PTG\\PME\\15C07\\Photos']
        self.output_table.directory_comboBox.insertItems(0, directory_list)
        self.output_table.table = self.parent.out_dir_tableWidget
        # self.output_table.table = self.parent.out_dir_tableWidget
        self.output_table.create_dir_table_data()
        self.output_table.table_from_list()

@@ -82,7 +95,7 @@ class pd_ui_class(PictureDirTable.Pic_Dir_Table):

    def output_transfer_selection(self):
        transfer_list = self.transfer_table.transfer_selection()
        output_path = self.output_table.output_directory_comboBox.text()  # self.output_table.directory_lineEdit.text()
        output_path = self.output_table.directory_comboBox.currentText()  # self.output_table.directory_lineEdit.text()
        increment_letter = self.parent.increment_letter_lineEdit.text()
        for i in range(len(transfer_list)):
            file_item = transfer_list[i]
@@ -107,7 +120,7 @@ class pd_ui_class(PictureDirTable.Pic_Dir_Table):
    def output_untransfer_selection(self):
        transfer_list = self.output_table.transfer_selection()
        # input_path = self.input_table.directory_lineEdit.text()
        input_path = self.input_table.directory_comboBox.text()
        input_path = self.input_table.directory_comboBox.currentText()
        for i in range(len(transfer_list)):
            file_item = transfer_list[i]
            new_file = input_path + '/' + file_item[0]
@@ -117,7 +130,7 @@ class pd_ui_class(PictureDirTable.Pic_Dir_Table):
                file_root = new_file[:dot_place]
                increment_letter = self.parent.increment_letter_lineEdit.text()
                for j in range(1000):
                    new_file = file_root + letter_increment(increment_letter, j) + file_type
                    new_file = str(file_root) + str(letter_increment(increment_letter, j)) + file_type
                    if os.path.exists(new_file) is False:
                        break
            # os.rename(file_item[2], new_file)