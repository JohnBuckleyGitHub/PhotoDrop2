import os
from PyQt4 import QtGui
from PyQt4 import QtCore
import PictureDirTable
import time
import math


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
        count = 0
        for i in range(len(transfer_list)):
            file_item = transfer_list[i]
            increment_letter = increment_letter
            file_type = file_item[0][file_item[0].find('.'):]
            new_name = (self.parent.prefix_lineEdit.text() + self.parent.run_number_spinBox.text() +
                        increment_letter + file_type)
            new_file = output_path + '/' + new_name
            os.rename(file_item[2], new_file)
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
            os.rename(file_item[2], new_file)
            file_item[0] = os.path.basename(new_file)
            file_item[2] = new_file
            transfer_list[i] = file_item
        self.transfer_table.add_selections(transfer_list)
        self.transfer_table.table_from_list()
        self.output_table.table_from_list()

# def letter_increment(letters, increment):
#     alphabet = 'abcdefghijklmnopqrstuvwxyz'
#     base = len(alphabet)
#     new_places = math.log(increment)/math.log(base)
#     old_places = len(letters)
#     carry_int = 0
#     new_string = ''
#     for place in range(old_places)
#         last_letter =  letters[place-1:place]
#         loc = alphabet.find(letter)+increment + carry_int
#         new_letter = alphabet[loc:loc+1]
#         carry_int = int(loc/base)
#     new_letter = 1

def alpha2num(letters):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alpha_places = len(letters)
    total = 1
    for place in range(alpha_places):
        cur_letter =  letters[alpha_places - place - 1]
        loc = alphabet.find(cur_letter)
        total += loc
    return total

def num2alpha(number):
    if number == 0:
        return 0
    elif number < 0:
        number = number * -1
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    base = len(alphabet)
    places = int(math.log(number)/math.log(base)+1)
    alpha_str = ''
    for numeral in range(places):
        remainder = number % (base ** (numeral+1))
        number -= remainder
        letter = alphabet[remainder-1]
        alpha_str = letter + alpha_str
    return alpha_str


