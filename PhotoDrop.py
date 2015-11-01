import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import ctypes
import io
sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets
import PhotoDropFunctions


class MyWindow(QtGui.QMainWindow, kustomWidgets.status_label_class):  # PhotoDropFunctions.pic_dir_table

    def __init__(self):
        super().__init__()
        uic.loadUi('PhotoDrop.ui', self)
        self.setWindowTitle('Photo Renamer')
        self.brush = kustomWidgets.brushstyle()
        self.input_dir = PhotoDropFunctions.pd_ui_class(self, "input")
        # self.input_dir.default_path()
        # self.input_dir.table_from_dir()

        self.show()
        self.signalMapper = QtCore.QSignalMapper(self)

        self.in_dir_tableWidget.cellDoubleClicked.connect(self.input_dir.load_picture)
        self.browse_input_pushButton.clicked.connect(self.input_dir.browse_directory)
        self.refresh_input_pushButton.clicked.connect(self.input_dir.refresh_table)
        self.transfer_input_trans_pushButton.clicked.connect(self.input_dir.transfer_selection)
        #  self.create_wrl_pushButton.clicked.connect(self.get_box_contents)
        #  self.max_color_horizontalSlider.valueChanged.connect(self.slider_change)
        #  self.color_spinBox.valueChanged.connect(self.spinbox_change)

    # def me_rows(self, row, col):
    #     print(row)
    #     print(col)
    #     self.input_dir.load_picture( row, col)



if __name__ == '__main__':
    myappid = 'PhotoDrop.Beta.0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = MyWindow()
    sys.exit(app.exec_())
