import sys
import os
from send2trash import send2trash
import glob
import time
import datetime
import fnmatch
import shutil
from PyQt4 import QtCore
from PyQt4 import QtGui
sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets


class Pic_Dir_Table(QtCore.QObject):  # QtGui.QWidget):

    def __init__(self, parent, name):  # , parent):
        super().__init__()  # parent)
        self.parent = parent
        self.name = name
        self.table_parameters()
        self.process_table_parameters()
        self.thread_pool = QtCore.QThreadPool()

    def setup_connects(self, grandparent, ui_dict):
        for key in ui_dict:
            setattr(self, key, getattr(grandparent, ui_dict[key]))
        self.table.cellDoubleClicked.connect(self.load_picture)
        self.checkbox.clicked.connect(self.table_from_list)
        self.drag_register = []
        self.table.itemLeft.connect(self.send_items_to_drag)
        output = int(self.parent.settings.value((self.name + '_checkbox'), QtCore.Qt.Unchecked))
        self.checkbox.setCheckState(output)
        if self.name is not 'output_table':
            self.table.itemDropped.connect(self.append_from_event)
            self.table.itemUrlPasted.connect(self.append_from_event)
            self.table.itemImageDelete.connect(self.delete_selection)
            if self.name is 'transfer_table':
                self.table.itemImagePasted.connect(self.parent.image_paste_into_transfer)
                # self.table.itemImageDelete.connect(self.parent.input_untransfer_selection)
            else:
                self.table.itemImagePasted.connect(self.save_image_from_paste)
                # self.table.itemImageDelete.connect(self.delete_selection)
        if self.name is not 'transfer_table':
            # self.directory_comboBox = TidyComboBox(self.primitive_comboBox, 10)
            self.directory_comboBox.max_items = 10
            self.init_sort_comboBox()
            self.sort_comboBox.setCurrentIndex(int(self.parent.settings.value(self.name + 'sort_comboBox', 0)))
            if self.parent.settings.value(self.name + '_combo_items', []):
                self.directory_comboBox.insertItems(0, self.parent.settings.value(self.name + '_combo_items', []))
                self.directory_comboBox.setCurrentIndex(int(self.parent.settings.value(
                                                        self.name + '_combo_items_index', 0)))
            self.browse_button.clicked.connect(self.browse_directory)
            self.refresh_button.clicked.connect(self.refresh_table)
            self.directory_comboBox.currentIndexChanged.connect(self.sort_directory_combobox)
            self.sort_comboBox.currentIndexChanged.connect(self.refresh_table)
        self.directory_path = kustomWidgets.dir_clean(self.directory_comboBox.currentText())

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
        self.save_table_state()
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
            item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            table.setItem(i, col, item)
            col = 1
            item = QtGui.QTableWidgetItem()
            if self.checkbox.isChecked():
                if self.picture_id(i) in self.parent.pixmap_buffer_dict:
                    item.setData(QtCore.Qt.DecorationRole, self.parent.pixmap_buffer_dict[self.picture_id(i)])
                else:
                    item.setData(QtCore.Qt.DisplayRole, self.pics_in_dir[i][1])
                    self.load_picture_from_runnable(self.pics_in_dir[i][2], col, i)
            else:
                item.setData(QtCore.Qt.DisplayRole, self.pics_in_dir[i][1])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            table.setItem(i, col, item)
        table.setSelectionBehavior(table.SelectRows)

    def create_dir_table_data(self):
        self.pics_in_dir = []
        if self.name is 'transfer_table':
            self.pics_in_dir = self.parent.transfer_table_list.copy()
            return
        self.directory_path = kustomWidgets.dir_clean(self.directory_comboBox.currentText())
        for pic_type in self.picture_type_list:
            tl = glob.glob(self.directory_path + '\\' + pic_type)
            for file_path in tl:
                file_pack = self.create_file_pack(file_path)
                if file_pack not in self.parent.transfer_table_list:
                    self.pics_in_dir.append(file_pack)
        (sort_index, reverse_boolean) = self.sort_dict[self.sort_comboBox.currentText()]
        self.pics_in_dir = sorted(self.pics_in_dir, key=lambda x: x[sort_index], reverse=reverse_boolean)

    def create_file_pack(self, file_path):
        filename = os.path.basename(file_path)
        creation_time = self.get_creation_times(file_path)
        modified_time = os.path.getmtime(file_path)
        return [filename, creation_time, file_path, modified_time]

    def append_from_event(self, event):
        if type(event) == QtGui.QDropEvent:
            # print("QDropEvent")
            if event.mimeData().urls():
                for urls in event.mimeData().urls():
                    print("got here")
                    file_path = urls.path()[1:]
                    self.add_file(file_path)
            try:
                for urls in event.urls():
                    file_path = urls.path()[1:]
                    self.add_file(file_path)
            else:
                dt = self.parent.drag_items_table
            if dt == 'input_table' and self.name == 'transfer_table':
                self.parent.input_transfer_selection()
            elif dt == 'transfer_table' and self.name == 'input_table':
                self.parent.input_untransfer_selection()
            elif dt == 'output_table' and self.name == 'transfer_table':
                self.parent.output_untransfer_selection()
            elif dt == 'transfer_table' and self.name == 'output_table':
                self.parent.output_untransfer_selection()
            else:
                print('hit the else condition')
                print(dt)
                print(self.name)
                return
        elif type(event) == QtCore.QMimeData:
            # print("QMimeData")
            for urls in event.urls():
                file_path = urls.path()[1:]
                self.add_file(file_path)
        elif type(event) == QtGui.QDragMoveEvent:
            
        else:
            print("somehow other: " + str(self.drag_register))
            print(type(event))
            return
        old_selections = self.table.selectionModel().selectedRows()
        self.refresh_table()
        self.parent.selection_carry(self.parent.transfer_table.table, old_selections)

    def add_file(self, file_path):
        file_name = file_path[file_path.rfind('/'):]
        new_file = self.directory_path + '\\' + file_name
        try:
            shutil.copy2(file_path, new_file)
        except shutil.SameFileError:
            file_format = new_file[new_file.rfind('.')+1:]
            new_file = self.highest_temp(file_format)
            shutil.copy2(file_path, new_file)
        if self.name == 'transfer_table':
            file_pack = self.create_file_pack(new_file)
            self.parent.transfer_table_list.append(file_pack)

    def save_image_from_paste(self, mime_data):
        file_format = 'jpg'
        qi = QtGui.QImageWriter()
        qi.setFormat(file_format)
        new_file = self.highest_temp(file_format)
        qi.setFileName(new_file)
        qi.write(mime_data.imageData())
        self.refresh_table()

    def highest_temp(self, file_format):
        file_prefix = 'Temp_'
        tl = glob.glob(self.directory_path + '\\' + file_prefix + '*')
        zeroes = 5
        for i in range(10 ** zeroes):
            z = kustomWidgets.zeronater(i, zeroes)
            if i >= len(tl):
                break
            if (z in os.path.basename(tl[i])) is False:
                break
        new_file = self.directory_path + '\\' + file_prefix + z + '.' + file_format
        return new_file

    def get_creation_times(self, fullname):
        c_time_sec = os.path.getctime(fullname)
        c_time_struct = datetime.datetime.fromtimestamp(c_time_sec)
        c_time_string = time.strftime("%Y.%m.%d \n%H:%M:%S", c_time_struct.timetuple())
        return c_time_string

    def load_picture_from_runnable(self, image_path, col_number, row_number):
        worker = LoadImageRunnable(image_path, self.col_width[col_number], self.row_height, col_number, row_number)
        self.connect(worker.signal, worker.signal.signal, self.show_picture_in_item)
        self.thread_pool.start(worker)

    def show_picture_in_item(self, image_scaled, col_number, row_number):
        pixmap = QtGui.QPixmap.fromImage(image_scaled)
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DecorationRole, pixmap)
        self.table.setItem(row_number, col_number, item)
        self.parent.pixmap_buffer_dict[self.picture_id(row_number)] = pixmap

    def picture_id(self, row):
        if row < len(self.pics_in_dir):
            try:
                return (str(self.pics_in_dir[row][0]) + "//" + str(self.pics_in_dir[row][3]))
            except IndexError:
                print("row = " + str(row))
        return "Row Unavailable"

    def load_picture(self, row, col):
        file_path = '"' + self.pics_in_dir[row][2] + '"'
        os.system(file_path)

    def browse_directory(self):
        new_directory_path = QtGui.QFileDialog.getExistingDirectory(None, '', self.directory_comboBox.currentText())
        self.directory_comboBox.combobox_tidy(new_directory_path)
        self.refresh_table()

    def sort_directory_combobox(self):
        self.directory_comboBox.combobox_sort()
        self.refresh_table()

    def refresh_table(self):
        self.create_dir_table_data()
        self.table_from_list()

    def add_selections(self, transfer_list):
        for flist in transfer_list:
            self.pics_in_dir.append(flist)

    def send_items_to_drag(self):
        self.drag_register = self.transfer_selection()
        self.parent.drag_items_table = self.name
        print(self.parent.drag_items_table)

    def transfer_selection(self):
        transfer_list = []
        indices = self.table.selectionModel().selectedRows()
        # indices = sorted(indices, key=lambda x: x.row(), reverse=True)
        for index in indices:
            transfer_list.append(self.pics_in_dir[index.row()])
        return transfer_list

    def delete_selection(self):
        indices = self.table.selectionModel().selectedRows()
        for del_num in indices:
            send2trash(self.pics_in_dir[del_num.row()][2])
        if self.name == 'transfer_table':
            self.parent.input_untransfer_selection()
        self.refresh_table()

    def save_table_state(self):
        if self.name is not 'transfer_table':
            self.parent.settings.setValue(self.name + 'sort_comboBox', self.sort_comboBox.currentIndex())
            if self.directory_comboBox.get_combo_items():
                self.parent.settings.setValue(self.name + '_combo_items', self.directory_comboBox.get_combo_items())
                self.parent.settings.setValue(self.name + '_combo_items_index', self.directory_comboBox.currentIndex())
        self.parent.settings.setValue(self.name + '_checkbox', str(self.checkbox.checkState()))

    def init_sort_comboBox(self):
        self.sort_dict = {'Date Created - Ascending': [1, False],
                          'Date Created - Descending': [1, True],
                          'Date Modified - Ascending': [3, False],
                          'Date Modified - Descending': [3, True],
                          'Name - Ascending': [0, False],
                          'Name - Descending': [0, True]}
        self.sort_comboBox.insertItems(0, sorted(self.sort_dict.keys()))


class SignalEmitter(QtCore.QObject):
    #  Needed because QRunnable does not emit a signal

    def __init__(self):
        super().__init__()
        self.signal = QtCore.SIGNAL("image_loaded_signal")


class LoadImageRunnable(QtCore.QRunnable):

    def __init__(self, image_path, col_width, row_height, col_number, row_number):
        super().__init__()
        self.signal = SignalEmitter()
        self.image_path = image_path
        self.col_width = col_width
        self.row_height = row_height
        self.col_number = col_number
        self.row_number = row_number

    def run(self):
        image = QtGui.QImage(self.image_path)
        image_scaled = image.scaled(self.col_width, self.row_height, QtCore.Qt.KeepAspectRatio)
        self.signal.emit(self.signal.signal, image_scaled, self.col_number, self.row_number)


