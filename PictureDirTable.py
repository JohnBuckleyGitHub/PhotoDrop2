import sys
import os
from send2trash import send2trash
import glob
import time
import datetime
import fnmatch
import threading
from PyQt4 import QtCore
from PyQt4 import QtGui
sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets
import kustomPalette


class Pic_Dir_Table(object):

    def __init__(self, parent):
        self.parent = parent
        self.checkbox = None
        self.table_parameters()
        self.process_table_parameters()
        self.mainThread = QtCore.QThread.currentThread()
        self.thread_list = []

    def table_parameters(self):
        # [Header Name, Column Width, Row Height] and None is flexible, Only Max row height is used
        self.table_params = [
                                        ['Filename', 150, None],
                                        ['Image', 300, 200],
                                        ]
        self.no_check_row_height = 40

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
            if self.checkbox.isChecked():
                table.setRowHeight(i, self.row_height)
                full_text = self.pics_in_dir[i][0] + "\n \n \n" + self.pics_in_dir[i][1]
            else:
                table.setRowHeight(i, self.no_check_row_height)
                full_text = self.pics_in_dir[i][0]
            col = 0
            full_text = self.pics_in_dir[i][0] + "\n \n \n" + self.pics_in_dir[i][1]
            item = QtGui.QTableWidgetItem(full_text)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            # if self.pics_in_dir[i][3]:
            # #     item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            #     item.setBackground(self.parent.brush.nobrush)
            # # else:
            # #     item.setFlags(QtCore.Qt.ItemIsEnabled)
            #     item.setBackground(self.parent.brush.grey)
            item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            # item.setTextAlignment(QtCore.Qt.AlignVCenter)
            table.setItem(i, col, item)
            col = 1
            if self.checkbox.isChecked():
                # item = self.load_picture_in_item(self.pics_in_dir[i][2], col)
                item = QtGui.QTableWidgetItem(self.pics_in_dir[i][1])
                self.load_picture_from_thread(self.pics_in_dir[i][2], col, i)
                # self.thread = QtCore.QThread()
                # image_thread = self.threaded_picture_loader(self, i, self.pics_in_dir[i][2], self.row_height,
                #                                             self.col_width[col], col)
                # self.threads += [image_thread]
                # image_thread.start()
            else:
                item = QtGui.QTableWidgetItem(self.pics_in_dir[i][1])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            # if self.pics_in_dir[i][3]:
            #     item.setBackground(self.parent.brush.nobrush)
            # else:
            # #     item.setFlags(QtCore.Qt.ItemIsEnabled)
            #     item.setBackground(self.parent.brush.grey)
            table.setItem(i, col, item)
        table.setSelectionBehavior(table.SelectRows)

    def create_dir_table_data(self):
        # self.directory_path = kustomWidgets.dir_clean(self.directory_lineEdit.text())
        self.directory_path = kustomWidgets.dir_clean(self.directory_comboBox.currentText())
        self.create_empty_table()
        for pic_type in self.picture_type_list:
            tl = glob.glob(self.directory_path + '/' + pic_type)
            for file_path in tl:
                filename = os.path.basename(file_path)
                creation_time = self.get_creation_times(file_path)
                self.pics_in_dir.append([filename, creation_time, file_path, True])
        self.pics_in_dir = sorted(self.pics_in_dir, key=lambda x: x[1])

    def append_dir_table(self, file_path):
        for pic_type in self.picture_type_list:
            if fnmatch.fnmatch(file_path, pic_type):
                filename = os.path.basename(file_path)
                creation_time = self.get_creation_times(file_path)
                self.pics_in_dir.append([filename, creation_time, file_path, True])
        self.table_from_list()

    def append_from_event(self, event):
        if type(event) == QtGui.QDropEvent:
            for urls in event.mimeData().urls():
                file_path = urls.path()[1:]
                self.append_dir_table(file_path)
        elif type(event) == QtCore.QMimeData:
            for urls in event.urls():
                file_path = urls.path()[1:]
                self.append_dir_table(file_path)
        elif type(event) == str:
            self.append_dir_table(event)

    def save_image_from_paste(self, mime_data):
        file_format = 'jpg'
        qi = QtGui.QImageWriter()
        qi.setFormat(file_format)
        new_file = self.highest_temp(file_format)
        qi.setFileName(new_file)
        qi.write(mime_data.imageData())
        self.append_from_event(new_file)

    def highest_temp(self, file_format):
        file_prefix = 'Temp_'
        tl = glob.glob(self.directory_path + '/' + file_prefix + '*')
        zeroes = 5
        for i in range(10 ** zeroes):
            z = kustomWidgets.zeronater(i, zeroes)
            if i >= len(tl):
                break
            if (z in os.path.basename(tl[i])) is False:
                break
        new_file = self.directory_path + '/' + file_prefix + z + '.' + file_format
        return new_file

    def add_selections(self, transfer_list):
        for flist in transfer_list:
            # flist[3] = True
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

    def load_picture_from_thread(self, image_path, col_number, row_number):
        thread = QtCore.QThread()
        worker = LoadImageThread(image_path, self.col_width[col_number], self.row_height, col_number, row_number)
        thread.started.connect(worker.start)
        worker.moveToThread(thread)
        # thread = LoadImageThread(image_path, self.col_width[col_number], self.row_height, col_number, row_number)
        # self.connect(thread, QtCore.SIGNAL("showImage(QString, int, int)"), self.showImage)
        thread.start()
        self.thread_list.append(thread)
        print("thread length" + str(len(self.thread_list)))

    def show_picture_in_item(self, image_scaled, col_number, row_number):
        print("even_here")
        pixmap = QtGui.QPixmap.fromImage(image_scaled)
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DecorationRole, pixmap)
        self.table.setItem(row_number, col_number, item)

    def load_picture(self, row, col):
        file_path = '"' + self.pics_in_dir[row][2] + '"'
        os.system(file_path)

    def browse_directory(self):
        new_directory_path = QtGui.QFileDialog.getExistingDirectory()
        # self.parent.input_directory_lineEdit.setText(new_directory_path)
        # self.directory_lineEdit.setText(new_directory_path)
        self.input_directory_comboBox.setText(new_directory_path)
        self.directory_comboBox.setText(new_directory_path)
        self.refresh_table()

    def refresh_table(self):
        self.create_dir_table_data()
        self.table_from_list()

    def transfer_selection(self):
        transfer_list = []
        indices = self.table.selectionModel().selectedRows()
        indices = sorted(indices, key=lambda x: x.row(), reverse=True)
        for index in indices:
            transfer_row = []
            for item in self.pics_in_dir[index.row()]:
                transfer_row.append(item)
            transfer_list.append(transfer_row)
            del self.pics_in_dir[index.row()]
            # self.pics_in_dir[index.row()][3] = False
        return transfer_list

    def delete_selection(self):
        indices = self.table.selectionModel().selectedRows()
        indices = sorted(indices, key=lambda x: x.row(), reverse=True)
        for del_num in indices:
            # os.remove(self.pics_in_dir[del_num.row()][2])
            send2trash(self.pics_in_dir[del_num.row()][2])
            del self.pics_in_dir[del_num.row()]
        self.table_from_list()

    def someFunctionCalledFromAnotherThread(self):
        thread = LoadImageThread(file="test.png", w=512, h=512)
        self.connect(thread, QtCore.SIGNAL("showImage(QString, int, int)"), self.showImage)
        thread.start()


    # class threaded_picture_loader(QtCore.QObject):
    #     # lock = threading.Lock()

    #     def __init__(self, parent, row, image_path, col_width, col_number):
    #         super(self.threaded_picture_loader, self).__init__()
    #         self.parent = parent
    #         self.row = row
    #         self.image_path = image_path
    #         self.row_height = row_height
    #         self.col_width = col_width
    #         self.col_number = col_number
    #         # PrimeNumber.lock.acquire()
    #         # PrimeNumber.prime_numbers[number] = "None"
    #         # PrimeNumber.lock.release()

    #     def run(self):
    #         image = QtGui.QImage(self.image_path)
    #         image_scaled = image.scaled(self.col_width, self.row_height, QtCore.Qt.KeepAspectRatio)
    #         output_object = (self.row, image_scaled)
    #         self.moveToThread(mainThread)
    #         self.parent.table.itemImageScaled.emit(output_object)
    #           # image_scaled)

class LoadImageThread(QtCore.QObject):

    def __init__(self, image_path, col_width, row_height, col_number, row_number):
        QtCore.QObject.__init__(self)
        self.image_path = image_path
        self.col_width = col_width
        self.row_height = row_height
        self.col_number = col_number
        self.row_number = row_number

    @QtCore.pyqtSlot()
    def start(self):
        print("got here")
        image = QtGui.QImage(self.image_path)
        image_scaled = image.scaled(self.col_width, self.row_height, QtCore.Qt.KeepAspectRatio)
        print("picture_scaled")
        self.emit(QtCore.SIGNAL('show_picture_in_item(QImage, int, int)'),
                  image_scaled, self.col_number, self.row_number)
