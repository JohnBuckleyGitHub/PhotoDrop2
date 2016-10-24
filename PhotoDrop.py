import PhotoDrop_DB
import sys
import sip
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

    def __init__(self, version):
        super().__init__()
        uic.loadUi('PhotoDrop.ui', self)  # disable for py2exe
        # self.setupUi(self)  # enable for py2exe
        self.setWindowTitle('Photo Drop ' + str(version))
        self.brush = kustomWidgets.brushstyle()
        self.db_window = PhotoDrop_DB.DataBaseWindow(self)
        self.db_window.set_connection()
        self.tables = PhotoDropFunctions.pd_ui_class(self)
        QtGui.QApplication.processEvents()
        self.show()
        # self.signalMapper = QtCore.QSignalMapper(self)

        self.pd_database_settings_pushButton.clicked.connect(self.db_window.show_window)


def run_prog():
    version = 'V1.14 - Commerical Trial'
    myappid = 'JPBaero.PhotoDrop.' + version  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    sip.setdestroyonexit(True)
    window = MyWindow(version)
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_prog()
