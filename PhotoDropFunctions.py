import sys
import os
import glob
import time
import datetime
from PyQt4 import QtCore
from PyQt4 import QtGui
sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets
import kustomPalette


class pd_functions_class(object):

    def __init__(self):
        pass

class pic_dir_table(object):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        print("got here")
        pass

    def default_path(self):
        self.parent.input_directory_lineEdit.setText('C:/Users/Johns Lenovo/Pictures')

    def table_parameters(self):
        # [Header Name, Column Width, Row Height] and None is flexible, Only Max row height is used
        self.table_params = [
                                        ['Filename', 150, None],
                                        ['Image', 300, 200],
                                        ]

    def process_table_parameters(self):
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

    def table_from_dir(self):
        #  This function populates a table from a query (originally a db quary)
        self.in_dir_table = self.parent.in_dir_tableWidget  # makes the table specific to this widget
        table = self.in_dir_table  # Shortcut for long name
        table.setRowCount(0)
        self.table_parameters()
        self.process_table_parameters()
        self.create_dir_table()
        table.setColumnCount(self.colcount)
        for col in range(self.colcount):
            self.in_dir_table.setColumnWidth(col, self.col_width[col])
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalHeaderLabels(self.header_labels)
        table.horizontalHeader().setMovable(False)
        for i in range(self.entry_count):
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
            image_path = self.input_path + self.pics_in_dir[i][0]
            item = self.load_picture_in_item(image_path, col)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            table.setItem(i, col, item)
        table.setSelectionBehavior(table.SelectRows)

    def create_dir_table(self):
        self.input_path = kustomWidgets.dir_clean(self.parent.input_directory_lineEdit.text())
        print(self.input_path)
        picture_type_list = ['*.png', '*.jpg', '*.gif', '*.bmp']
        self.pics_in_dir = []
        self.entry_count = 0
        for pic_type in picture_type_list:
            tl = glob.glob(self.input_path + '/' + pic_type)
            for inst in tl:
                filename = os.path.basename(inst)
                creation_time = self.get_creation_times(filename)
                self.pics_in_dir.append([filename, creation_time])
                self.entry_count += 1
        self.pics_in_dir = sorted(self.pics_in_dir, key=lambda x: x[1])

    def get_creation_times(self, filename):
        fullname = self.input_path + filename
        c_time_sec = os.path.getctime(fullname)
        c_time_struct = datetime.datetime.fromtimestamp(c_time_sec)
        c_time_string = time.strftime("%Y.%m.%d \n%H:%M:%S", c_time_struct.timetuple())
        return c_time_string

    def load_picture_in_item(self, image_path, col_number):
        #  image_path = '"' + image_path + '"'

       #  image_path = image_path.replace("/", "\\")

        print(image_path)
        image = QtGui.QImage(image_path)
        image_scaled = image.scaled(self.col_width[col_number], self.row_height, QtCore.Qt.KeepAspectRatio)
        pixmap = QtGui.QPixmap.fromImage(image_scaled)
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DecorationRole, pixmap)
        return item

    def load_picture(self, row, col):
        file_path = '"' + self.input_path + self.pics_in_dir[row][0] + '"'
        os.system(file_path)

    def browse_directory(self):
        print("got here")
        inputpath = QtGui.QFileDialog.getExistingDirectory()
        self.parent.input_directory_lineEdit.setText(inputpath)
        self.refresh_table()

    def refresh_table(self):
        self.table_from_dir()




    # def get_box_contents(self):
    #     self.comparison_parts = []
    #     box_contents = self.BL_plainTextEdit.toPlainText()
    #     print(box_contents)
    #     self.baseline_parts = self.create_list(box_contents)
    #     self.comparison_parts.append(self.create_list(self.Compare_plainTextEdit.toPlainText()))
    #     output_filename = self.file_out_lineEdit.text()
    #     output_directory = self.path_out_lineEdit.text()
    #     if (not output_directory[len(output_directory)-1:] == '/' and
    #         not output_directory[len(output_directory)-2:] == '\\'):
    #         output_directory += '/'
    #     self.output_full = output_directory + output_filename
    #     if self.baseline_parts:
    #         bl_exists = True
    #         self.comparison_parts.insert(0, self.baseline_parts)
    #     else:
    #         bl_exists = False
    #     try:
    #         os.remove(self.output_full)
    #         print(self.output_full + " file overwritten")
    #     except FileNotFoundError:
    #         print("New file created: " + self.output_full)
    #         pass
    #     wrlm.wrl_stitch(self.output_full, self.comparison_parts, 'W:/Production/WRL Files',
    #                     bl_exists, color=(self.color_current, self.number_of_colors))
    #     if self.open_wrl_checkBox.isChecked():
    #         os.system(self.output_full)

    # def create_list(self, box_contents):
    #     print(box_contents)
    #     box_lines = []
    #     for i in range(1000):
    #         end_of_line = box_contents.find('\n')
    #         if end_of_line < 0:
    #             end_of_line = len(box_contents)
    #         box_lines.append(box_contents[:end_of_line])
    #         box_contents = box_contents[end_of_line+1:]
    #         if len(box_contents) <= 3:
    #             break
    #     return box_lines


    # def set_slider(self):
    #     self.max_color_horizontalSlider.setRange(4, 30)
    #     self.max_color_horizontalSlider.setSingleStep(1)
    #     self.max_color_horizontalSlider.setValue(10)
    #     self.number_of_colors = self.max_color_horizontalSlider.sliderPosition()

    # def slider_change(self):
    #     self.number_of_colors = self.max_color_horizontalSlider.sliderPosition()
    #     self.max_color_lcdNumber.display(self.number_of_colors)
    #     self.sc.compute_initial_figure(self.number_of_colors)
    #     self.spinbox_change()
    #     self.color_spinBox.setMinimum(1)
    #     self.color_spinBox.setMaximum(self.number_of_colors)

    # def palette_set(self):
    #     self.palette_obj = WAE_palette.palette(self.number_of_colors)

    # def spinbox_init(self):
    #     self.color_spinBox.setMinimum(1)
    #     self.color_spinBox.setMaximum(self.number_of_colors)
    #     self.color_spinBox.setValue(1)
    #     self.palette_set()
    #     self.spinbox_change()

    # def spinbox_change(self):
    #     self.palette_set()
    #     self.color_current = int(self.color_spinBox.value()) - 1
    #     the_window = self.Compare_plainTextEdit
    #     the_window.setAutoFillBackground(True)
    #     color_tuple = tuple(i * 255 for i in self.palette_obj.cmap_rgb[self.color_current])
    #     first_bit = """
    #     .QPlainTextEdit {
    #         background-color: rgb"""
    #     second_bit = """;
    #         }
    #         """
    #     full_str = first_bit + str(color_tuple) + second_bit
    #     the_window.setStyleSheet(full_str)


# class MyMplCanvas(FigureCanvas):

#     """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

#     def __init__(self, parent=None, width=500, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.aspect_ratio = (height/width)
#         self.axes = fig.add_subplot(111, aspect=self.aspect_ratio)
#         # We want the axes cleared every time plot() is called
#         # self.axes.hold(False)
#         self.fig = fig
#         # self.compute_initial_figure()
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)
#         FigureCanvas.setSizePolicy(self,
#                                    QtGui.QSizePolicy.Fixed,
#                                    QtGui.QSizePolicy.Fixed)
#         FigureCanvas.updateGeometry(self)


# class MyDynamicMplCanvas(MyMplCanvas):

#     def __init__(self, *args, **kwargs):
#         MyMplCanvas.__init__(self, *args, **kwargs)
#         # self.compute_initial_figure()

#     def compute_initial_figure(self, number_of_colors=10):
#         N = number_of_colors
#         self.axes.aspect_ratio = 1
#         self.axes.set_xlim([0, N])
#         self.axes.set_ylim([-.5*N/10, 0.5*N/10])
#         pal = WAE_palette.palette(N)
#         for i in range(N):
#             col = pal.cmap_rgb_brightness(i)
#             rect = plt.Rectangle((i, -.5*N/10), 1, N/10, facecolor=col)
#             self.axes.add_artist(rect)
#         labels = range(1, N+1)
#         self.axes.xaxis.set(ticks=arange(0.5, len(labels)), ticklabels=labels)
#         for tic in self.axes.xaxis.get_major_ticks():
#             tic.tick1On = tic.tick2On = False
#         self.axes.set_yticks([])
#         self.fig.patch.set_visible(False)
#         self.axes.plot()
#         self.draw()
