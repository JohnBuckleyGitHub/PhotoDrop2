import os
from PyQt4 import QtGui
from PyQt4 import QtCore
import PictureDirTable
import time
import math
import shutil
from send2trash import send2trash


class pd_ui_class(PictureDirTable.Pic_Dir_Table):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.input_table()
        self.transfer_table()
        self.output_table()

    def input_table(self):
        self.input_table = PictureDirTable.Pic_Dir_Table(self.parent)
        self.input_table.checkbox = self.parent.input_checkBox
        # self.input_table.parent = self.parent
        self.input_table.directory_lineEdit = self.parent.input_directory_lineEdit
        self.input_table.directory_lineEdit.setText('C:/Users/Johns Lenovo/Documents/Pictures/I15C07 SW SOS')
        self.input_table.table = self.parent.in_dir_tableWidget
        self.input_table.create_dir_table_data()
        self.input_table.table_from_list()

    def transfer_table(self):
        self.transfer_table = PictureDirTable.Pic_Dir_Table(self.parent)
        self.transfer_table.checkbox = self.parent.transfer_checkBox
        # self.transfer_table.parent = self.parent
        self.transfer_table.table = self.parent.transfer_tableWidget
        self.transfer_table.create_empty_table()

    def output_table(self):
        self.output_table = PictureDirTable.Pic_Dir_Table(self.parent)
        self.output_table.checkbox = self.parent.output_checkBox
        # self.transfer_table.parent = self.parent
        self.output_table.directory_lineEdit = self.parent.output_directory_lineEdit
        self.output_table.directory_lineEdit.setText('C:/Users/Johns Lenovo/Documents/Pictures')
        self.output_table.table = self.parent.out_dir_tableWidget
        self.output_table.create_dir_table_data()
        self.output_table.table_from_list()

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

    def output_transfer_selection(self):
        transfer_list = self.transfer_table.transfer_selection()
        output_path = self.output_table.directory_lineEdit.text()
        increment_letter = self.parent.increment_letter_lineEdit.text()
        for i in range(len(transfer_list)):
            file_item = transfer_list[i]
            file_type = file_item[0][file_item[0].find('.'):]
            for j in range(1000):
                inc_letter = letter_increment(increment_letter, j+1)
                new_name = (self.parent.prefix_lineEdit.text() + self.parent.run_number_spinBox.text() +
                            inc_letter + file_type)
                new_file = output_path + '/' + new_name
                if os.path.exists(new_file) is False:
                    break
            # os.rename(file_item[2], new_file)
            shutil.copy2(file_item[2], new_file)
            send2trash(file_item[2])
            file_item[0] = os.path.basename(new_file)
            file_item[2] = new_file
            transfer_list[i] = file_item
        self.output_table.add_selections(transfer_list)
        self.transfer_table.table_from_list()
        self.output_table.table_from_list()

    def output_untransfer_selection(self):
        transfer_list = self.output_table.transfer_selection()
        input_path = self.input_table.directory_lineEdit.text()
        for i in range(len(transfer_list)):
            file_item = transfer_list[i]
            new_file = input_path + '/' + file_item[0]
            if os.path.exists(new_file):
                dot_place = new_file.find('.')
                file_type = new_file[dot_place:]
                file_root = new_file[:dot_place]
                increment_letter = self.parent.increment_letter_lineEdit.text()
                for j in range(1000):
                    new_file = file_root + letter_increment(increment_letter, j) + file_type
                    if os.path.exists(new_file) is False:
                        break
            # os.rename(file_item[2], new_file)
            shutil.copy2(file_item[2], new_file)
            send2trash(file_item[2])
            file_item[0] = os.path.basename(new_file)
            file_item[2] = new_file
            transfer_list[i] = file_item
        self.transfer_table.add_selections(transfer_list)
        self.transfer_table.table_from_list()
        self.output_table.table_from_list()


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

# def baseN(num, b, numerals=alphabet()):
#     return (((num == 0) and numerals[0]) or
#             (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b]))


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

