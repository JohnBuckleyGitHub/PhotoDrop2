import os
from PyQt4 import QtGui
from PyQt4 import QtCore
import PictureDirTable
import shutil
from send2trash import send2trash
import kustomWidgets


class pd_ui_class(QtCore.QObject):

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.transfer_table_list = []
        self.pixmap_buffer_dict = {}
        self.active_table = None
        self.est_run_buffer_dict = {}
        self.init_settings()
        self.input_table()
        self.transfer_table()
        self.output_table()
        self.table_connects()

    def init_settings(self):
        self.settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.parent.pd_run_number_spinBox.setValue(int(self.settings.value('pd_run_number_spinBox', 0)))
        self.parent.pd_prefix_lineEdit.setText(self.settings.value('pd_prefix_lineEdit', 'Session Name here'))
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
        self.input_table.refresh_table()

    def transfer_table(self):
        ui_dict = {'table': 'transfer_tableWidget',
                   'checkbox': 'transfer_checkBox',
                   'directory_comboBox': 'input_directory_comboBox'}
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
        self.output_table.refresh_table()

    def table_connects(self):
        self.parent.pd_transfer_input_trans_pushButton.clicked.connect(self.input_transfer_selection)
        self.parent.pd_untransfer_input_trans_pushButton.clicked.connect(self.input_untransfer_selection)
        self.parent.pd_transfer_output_trans_pushButton.clicked.connect(self.output_transfer_selection)
        self.parent.pd_untransfer_output_trans_pushButton.clicked.connect(self.output_untransfer_selection)
        self.parent.pd_last_run_pushButton.clicked.connect(self.retrieve_last_run_number)
        self.switch_move_or_copy()  # to init text
        self.parent.pd_move_or_copy_pushButton.clicked.connect(self.switch_move_or_copy)
        #  State Saves
        self.parent.pd_run_number_spinBox.valueChanged.connect(self.save_state)
        self.parent.pd_prefix_lineEdit.textChanged.connect(self.save_state)
        self.parent.pd_increment_letter_lineEdit.textChanged.connect(self.save_state)

    def save_state(self):
        self.settings.setValue('pd_run_number_spinBox', self.parent.pd_run_number_spinBox.value())
        self.settings.setValue('pd_prefix_lineEdit', self.parent.pd_prefix_lineEdit.text())
        self.settings.setValue('pd_increment_letter_lineEdit', self.parent.pd_increment_letter_lineEdit.text())

    def check_db_connection(self):
        self.parent.pd_last_run_pushButton.setEnabled(self.parent.run_db_conn.status)

    def retrieve_last_run_number(self):
        last_run = self.parent.run_db_conn.last_run()
        self.parent.pd_run_number_spinBox.setValue(int(last_run))

    def update_run_time_dict(self):
        self.parent.run_db_conn.get_run_time_dict()

    def input_transfer_selection(self):
        selection_list = self.input_table.transfer_selection()
        self.transfer_table_list.extend(selection_list)
        self.transfer_table.refresh_table()
        sel_pics_list = [item[0] for item in selection_list]
        self.selection_carry(self.transfer_table.table, sel_pics_list)
        self.input_table.refresh_table()

    def input_untransfer_selection(self):
        selection_list = self.transfer_table.transfer_selection()
        for file_pack in selection_list:
            self.transfer_table_list.remove(file_pack)
        self.transfer_table.refresh_table()
        self.input_table.refresh_table()

    def image_paste(self, mime_data):
        filename_list = self.input_table.save_image_from_paste(mime_data)
        self.selection_carry(self.input_table.table, filename_list)
        if self.active_table is 'transfer_table':
            self.input_transfer_selection()
        elif self.active_table is 'output_table':
            self.input_transfer_selection()
            self.output_transfer_selection()

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
                run_number = kustomWidgets.zeronater(int(self.parent.pd_run_number_spinBox.text()), 4)
                # run_number = self.parent.pd_run_number_spinBox.text()
                new_name = (self.parent.pd_prefix_lineEdit.text() + run_number +
                            inc_letter + file_type)
                print(new_name)
                new_file = output_path + '/' + new_name
                if os.path.exists(new_file) is False:
                    break
            shutil.copy2(file_item[2], new_file)
            if self.is_switch_move():
                send2trash(file_item[2])
        self.input_table.refresh_table()
        self.transfer_table.refresh_table()
        self.output_table.refresh_table()

    def output_untransfer_selection(self):
        selection_list = self.output_table.transfer_selection()
        select_list_carry = []
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
            if self.is_switch_move():
                send2trash(file_item[2])
            file_pack = self.transfer_table.create_file_pack(new_file)
            self.transfer_table_list.append(file_pack)
            select_list_carry.append(new_file[new_file.rfind("\\")+1:])
        self.input_table.refresh_table()
        self.transfer_table.refresh_table()
        self.selection_carry(self.transfer_table.table, select_list_carry)
        self.output_table.refresh_table()

    def switch_move_or_copy(self):
        if self.is_switch_move():
            button = "Move"
            switch = "Copy"
        else:
            button = "Copy"
            switch = "Move"
        button_str = "Switch to " + button
        label_str = switch + "\nbetween directories"
        self.parent.pd_move_or_copy_pushButton.setText(button_str)
        self.parent.pd_move_or_copy_label.setText(label_str)

    def is_switch_move(self):
        if 'Move' in self.parent.pd_move_or_copy_label.text():
            return True
        else:
            return False

    def selection_carry(self, table, selection_list):
        model = table.model()
        sel_model = table.selectionModel()
        for t_row in range(model.rowCount()):
            data = model.index(t_row, 0).data(0)  # 0 in data(0) being the Qt::DisplayRole
            pic_name = data[:data.find('\n')]
            if pic_name in selection_list:
                sel_model.select(model.index(t_row, 0), (QtGui.QItemSelectionModel.Select |
                                                         QtGui.QItemSelectionModel.Rows))


def letter_increment(letters, increment):
    init_value = alpha2num(letters.lower())
    new_letters = num2alpha(init_value + increment)
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
