import os
from PyQt4 import QtGui
from PyQt4 import QtCore
import PictureDirTable
import shutil
from send2trash import send2trash


class pd_ui_class(QtCore.QObject):

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.transfer_table_list = []
        self.pixmap_buffer_dict = {}
        self.init_settings()
        self.input_table()
        self.transfer_table()
        self.output_table()
        self.table_connects()

    def init_settings(self):
        # self.settings = QtCore.QSettings('abc', 'def')
        self.settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.parent.pd_run_number_spinBox.setValue(int(self.settings.value('pd_run_number_spinBox', 0)))
        self.parent.pd_prefix_lineEdit.setText(self.settings.value('pd_prefix_lineEdit', 'I15C08'))
        self.parent.pd_increment_letter_lineEdit.setText(self.settings.value('pd_increment_letter_lineEdit', 'aa'))

    def input_table(self):
        ui_dict = {'table': 'input_directory_tableWidget',
                   'browse_button': 'input_browse_pushButton',
                   'refresh_button': 'input_refresh_pushButton',
                   'checkbox': 'input_picture_checkBox',
                   'directory_comboBox': 'input_directory_comboBox',
                   'sort_comboBox': 'input_sort_comboBox'}
        self.input_table = PictureDirTable.Pic_Dir_Table(self, 'input_table')
        self.input_table.setup_connects(self.parent, ui_dict)
        self.input_table.create_dir_table_data()
        self.input_table.table_from_list()

    def transfer_table(self):
        ui_dict = {'table': 'transfer_tableWidget',
                   'checkbox': 'transfer_checkBox'}
        self.transfer_table = PictureDirTable.Pic_Dir_Table(self, 'transfer_table')  # self.parent)
        self.transfer_table.setup_connects(self.parent, ui_dict)
        self.transfer_table.pics_in_dir = []

    def output_table(self):
        ui_dict = {'table': 'output_directory_tableWidget',
                   'browse_button': 'output_browse_pushButton',
                   'refresh_button': 'output_refresh_pushButton',
                   'checkbox': 'output_picture_checkBox',
                   'directory_comboBox': 'output_directory_comboBox',
                   'sort_comboBox': 'output_sort_comboBox'}
        self.output_table = PictureDirTable.Pic_Dir_Table(self, 'output_table')  # self.parent)
        self.output_table.setup_connects(self.parent, ui_dict)
        self.output_table.create_dir_table_data()
        self.output_table.table_from_list()

    def table_connects(self):
        self.parent.pd_transfer_input_trans_pushButton.clicked.connect(self.input_transfer_selection)
        self.parent.pd_untransfer_input_trans_pushButton.clicked.connect(self.input_untransfer_selection)
        self.parent.pd_transfer_output_trans_pushButton.clicked.connect(self.output_transfer_selection)
        self.parent.pd_untransfer_output_trans_pushButton.clicked.connect(self.output_untransfer_selection)
        self.parent.pd_last_run_pushButton.clicked.connect(self.retrieve_last_run_number)
        self.parent.pd_run_number_spinBox.valueChanged.connect(self.save_state)
        self.parent.pd_prefix_lineEdit.textChanged.connect(self.save_state)
        self.parent.pd_increment_letter_lineEdit.textChanged.connect(self.save_state)

    def save_state(self):
        self.settings.setValue('pd_run_number_spinBox', self.parent.pd_run_number_spinBox.value())
        self.settings.setValue('pd_prefix_lineEdit', self.parent.pd_prefix_lineEdit.text())
        self.settings.setValue('pd_increment_letter_lineEdit', self.parent.pd_increment_letter_lineEdit.text())

    def retrieve_last_run_number(self):
        self.save_state()

    def input_transfer_selection(self):
        selection_list = self.input_table.transfer_selection()
        self.transfer_table_list.extend(selection_list)
        # self.transfer_table.add_selections(selection_list)
        t = self.transfer_table.table
        self.transfer_table.refresh_table()
        # self.transfer_table.table.selectRow(2)
        # self.transfer_table.table.selectRows(0,2)
        t.selectionModel().select(t.model().index(0,0), (QtGui.QItemSelectionModel.SelectCurrent | QtGui.QItemSelectionModel.Rows))
        t.selectionModel().select(t.model().index(1,1), (QtGui.QItemSelectionModel.Select | QtGui.QItemSelectionModel.Rows))
        #  t.item(0,0).setSelected(True)
        #  t.item(2,0).setSelected(True)
        self.input_table.refresh_table()

    def input_untransfer_selection(self):
        selection_list = self.transfer_table.transfer_selection()
        for file_pack in selection_list:
            self.transfer_table_list.remove(file_pack)
        # self.input_table.add_selections(selection_list)
        self.transfer_table.refresh_table()
        self.input_table.refresh_table()

    def image_paste_into_transfer(self, mime_data):
        self.parent.input_directory_tableWidget.itemImagePasted.emit(mime_data)
        last_row = self.parent.input_directory_tableWidget.rowCount() - 1
        for col in range(self.parent.input_directory_tableWidget.columnCount()):
            self.parent.input_directory_tableWidget.item(last_row, col).setSelected(True)
        self.input_transfer_selection()

    def output_transfer_selection(self):
        selection_list = self.transfer_table.transfer_selection()
        for file_pack in selection_list:
            self.transfer_table_list.remove(file_pack)
        output_path = self.output_table.directory_comboBox.currentText()  # self.output_table.directory_lineEdit.text()
        increment_letter = self.parent.pd_increment_letter_lineEdit.text()
        for i in range(len(selection_list)):
            file_item = selection_list[i]
            file_type = file_item[0][file_item[0].find('.'):]
            for j in range(1000):
                inc_letter = letter_increment(increment_letter, j)
                new_name = (self.parent.pd_prefix_lineEdit.text() + self.parent.pd_run_number_spinBox.text() +
                            inc_letter + file_type)
                new_file = output_path + '/' + new_name
                if os.path.exists(new_file) is False:
                    break
            # os.rename(file_item[2], new_file)
            shutil.copy2(file_item[2], new_file)
            send2trash(file_item[2])
            file_item[0] = os.path.basename(new_file)
            file_item[2] = new_file
            selection_list[i] = file_item
        self.input_table.refresh_table()
        self.transfer_table.refresh_table()
        self.output_table.refresh_table()

    def output_untransfer_selection(self):
        selection_list = self.output_table.transfer_selection()
        input_path = self.input_table.directory_comboBox.currentText()
        for i in range(len(selection_list)):
            file_item = selection_list[i]
            new_file = input_path + '\\' + file_item[0]
            if os.path.exists(new_file):
                dot_place = new_file.find('.')
                file_type = new_file[dot_place:]
                file_root = new_file[:dot_place]
                increment_letter = self.parent.pd_increment_letter_lineEdit.text()
                for j in range(1000):
                    new_file = str(file_root) + str(letter_increment(increment_letter, j)) + file_type
                    if os.path.exists(new_file) is False:
                        break
            shutil.copy2(file_item[2], new_file)
            send2trash(file_item[2])
            file_pack = self.transfer_table.create_file_pack(new_file)
            self.transfer_table_list.append(file_pack)
        self.input_table.refresh_table()
        self.transfer_table.refresh_table()
        self.output_table.refresh_table()


def letter_increment(letters, increment):
    init_value = alpha2num(letters.lower())
    # places = len(letters)
    new_letters = num2alpha(init_value + increment)
    # new_places = len(new_letters)
    # if (places - new_places) > 0:
    #     new_letters = letters[:places-new_places] + new_letters
    if letters.isupper():
        new_letters = new_letters.upper()
    return new_letters


def alpha2num(letters):
    abet = alphabet()
    base = len(abet)
    alpha_places = len(letters)
    total = 0
    for place in range(alpha_places):
        cur_letter = letters[alpha_places - place - 1]
        loc = abet.find(cur_letter) + 1
        total += (loc*(base**place))
    return total


def num2alpha(num):
    numerals = alphabet()
    base = len(numerals)
    s = ''
    if num == 0:
        return 0
    num -= 1  # since 0 is 0 and A is 1
    for i in range(20):
        s = numerals[int(num % base)] + s
        num = num / base
        if num < 1:
            break
        num -= 1
    return s


def alphabet():
    return 'abcdefghijklmnopqrstuvwxyz'


def debug_print():
    print("Debug print")
