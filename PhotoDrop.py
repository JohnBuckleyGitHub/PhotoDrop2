import PhotoDrop_DB
import sys
from PyQt4 import QtGui
# from PyQt4 import QtCore
from PyQt4 import uic  # disable for py2exe
import ctypes
# sys.path.insert(0, 'C:/Python Files/pythonlibs')
import kustomWidgets
import PhotoDropFunctions
# import photoDropUI  # enable for py2exe


class MyWindow(QtGui.QMainWindow, kustomWidgets.status_label_class):
    # class MyWindow(QtGui.QMainWindow, kustomWidgets.status_label_class,
    #                photoDropUI.Ui_MainWindow):  # enable for py2exe

    def __init__(self):
        super().__init__()
        uic.loadUi('PhotoDrop.ui', self)  # disable for py2exe
        # self.setupUi(self)  # enable for py2exe
        self.setWindowTitle('Photo Renamer')
        self.brush = kustomWidgets.brushstyle()
        self.tables = PhotoDropFunctions.pd_ui_class(self)
        self.db_window = PhotoDrop_DB.DataBaseWindow()
        self.show()
        # self.signalMapper = QtCore.QSignalMapper(self)

        self.pd_database_settings_pushButton.clicked.connect(self.db_window.show_window)


if __name__ == '__main__':
    myappid = 'Photinput_tableoDrop.Beta.0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = MyWindow()
    sys.exit(app.exec_())
