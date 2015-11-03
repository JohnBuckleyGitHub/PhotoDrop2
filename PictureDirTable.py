import sys
import os
import glob
import time
import datetime
import fnmatch
from PyQt4 import QtCore
from PyQt4 import QtGui
sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets
import kustomPalette


class Pic_Dir_Table(object):

    def __init__(self):
        self.parent = None
        self.table_parameters()
        self.process_table_parameters()

    def table_parameters(self):
        # [Header Name, Column Width, Row Height] and None is flexible, Only Max row height is used
        self.table_params = [
                                        ['Filename', 150, None],
                                        ['Image', 300, 200],
                                        ]

    def process_table_parameters(self):
        self.picture_type_list = ['*.png', '*.jpg', '*.gif', '*.bmp', '*.tif', '*.tiff']
        self.colcount = len(self.table_params)
        self.row_height = None
        self.header_labels = []
        self.col_width = []
        for params in self.table_params:
            self.header_labels.append(params[0])
            self.col_width.append(params[1])
            cur_row_height = params[2]
            if cur_row_height:
                if self.row_height:
                    if cur_row_height > self.row_height:
                        self.row_height = cur_row_height
                else:
                    self.row_height = cur_row_height  # No row height exists yet

    def table_from_list(self):
        #  This function populates a table from a query (originally a db quary)
        # self.in_dir_table = self.parent.in_dir_tableWidget  # makes the table specific to this widget
        table = self.table  # Shortcut for long name
        table.setRowCount(0)
        # self.create_dir_table_data()
        table.setColumnCount(self.colcount)
        for col in range(self.colcount):
            table.setColumnWidth(col, self.col_width[col])
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalHeaderLabels(self.header_labels)
        table.horizontalHeader().setMovable(False)
        for i in range(len(self.pics_in_dir)):
            table.insertRow(i)
            table.setRowHeight(i, self.row_height)
            col = 0
            full_text = self.pics_in_dir[i][0] + "\n \n \n" + self.pics_in_dir[i][1]
            item = QtGui.QTableWidgetItem(full_text)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            # item.setTextAlignment(QtCore.Qt.AlignVCenter)
            table.setItem(i, col, item)
            col = 1
            item = self.load_picture_in_item(self.pics_in_dir[i][2], col)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            table.setItem(i, col, item)
        table.setSelectionBehavior(table.SelectRows)

    def create_dir_table_data(self):
        self.directory_path = kustomWidgets.dir_clean(self.directory_lineEdit.text())
        self.create_empty_table()
        for pic_type in self.picture_type_list:
            tl = glob.glob(self.directory_path + '/' + pic_type)
            for file_path in tl:
                filename = os.path.basename(file_path)
                creation_time = self.get_creation_times(file_path)
                self.pics_in_dir.append([filename, creation_time, file_path])
        self.pics_in_dir = sorted(self.pics_in_dir, key=lambda x: x[1])

    def append_dir_table(self, file_path):
        for pic_type in self.picture_type_list:
            if fnmatch.fnmatch(file_path, pic_type):
                print("we have a match!")
                filename = os.path.basename(file_path)
                creation_time = self.get_creation_times(file_path)
                self.pics_in_dir.append([filename, creation_time, file_path])
            else:
                print("no dice!")
        self.table_from_list()

    def append_from_event(self, event):
        for urls in event.mimeData().urls():
            file_path = urls.path()[1:]
            self.append_dir_table(file_path)
            print(file_path)

    def add_selections(self, transfer_list):
        for flist in transfer_list:
            self.pics_in_dir.append(flist)

    def create_empty_table(self):
        self.pics_in_dir = []

    def get_creation_times(self, fullname):
        c_time_sec = os.path.getctime(fullname)
        c_time_struct = datetime.datetime.fromtimestamp(c_time_sec)
        c_time_string = time.strftime("%Y.%m.%d \n%H:%M:%S", c_time_struct.timetuple())
        return c_time_string

    def load_picture_in_item(self, image_path, col_number):
        image = QtGui.QImage(image_path)
        image_scaled = image.scaled(self.col_width[col_number], self.row_height, QtCore.Qt.KeepAspectRatio)
        pixmap = QtGui.QPixmap.fromImage(image_scaled)
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DecorationRole, pixmap)
        return item

    def load_picture(self, row, col):
        file_path = '"' + self.pics_in_dir[row][2] + '"'
        os.system(file_path)

    def browse_directory(self):
        new_directory_path = QtGui.QFileDialog.getExistingDirectory()
        self.parent.input_directory_lineEdit.setText(new_directory_path)
        self.directory_lineEdit.setText(new_directory_path)
        self.refresh_table()

    def refresh_table(self):
        self.create_dir_table_data()
        self.table_from_list()

    def transfer_selection(self):
        indices = self.table.selectionModel().selectedRows()
        transfer_list = []
        for index in indices:
            transfer_list.append(self.pics_in_dir[index.row()])
        return transfer_list

