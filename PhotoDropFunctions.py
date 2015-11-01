import PictureDirTable


class pd_ui_class(PictureDirTable.Pic_Dir_Table):

    def __init__(self, parent, ui_section):
        super().__init__()
        self.parent = parent
        # self.ui_dict = {}
        if "input" in ui_section.lower():
            self.input_table()
        self.table_from_list()

    def input_table(self):
        self.directory_lineEdit = self.parent.input_directory_lineEdit
        self.directory_lineEdit.setText('C:/Users/Johns Lenovo/Pictures')
        self.table = self.parent.in_dir_tableWidget
        self.create_dir_table_data()


    # def transfer_selection(self):
    #     selection_list = []
    #     for selec in 




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
