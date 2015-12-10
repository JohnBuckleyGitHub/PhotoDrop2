from PyQt4 import QtCore
from PyQt4 import QtGui


class TableWithPaste(QtGui.QTableWidget):

    itemDropped = QtCore.pyqtSignal(object)
    itemUrlPasted = QtCore.pyqtSignal(object)
    itemImagePasted = QtCore.pyqtSignal(object)
    itemImageDelete = QtCore.pyqtSignal(object)
    # itemImageScaled = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        QtGui.QTableWidget.__init__(self, parent)
        # super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # quitAction = QtGui.QAction("Quit", self)
        # quitAction.triggered.connect(QtGui.qApp.quit)

        pasteAction = QtGui.QAction("Paste", self)
        pasteAction.triggered.connect(self.getPastin)

        deleteAction = QtGui.QAction("Delete File", self)
        deleteAction.triggered.connect(self.deletePicFile)

        self.addAction(pasteAction)
        self.addAction(deleteAction)
        # self.addAction(quitAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            self.itemDropped.emit(event)
        else:
            event.ignore()

    def getPastin(self):
        clipboard = QtGui.qApp.clipboard().mimeData()
        if clipboard.hasUrls():
            self.itemUrlPasted.emit(clipboard)
        elif clipboard.hasImage():
            self.itemImagePasted.emit(clipboard)

    def deletePicFile(self):
        indices = self.selectionModel().selectedRows()
        self.itemImageDelete.emit(indices)
