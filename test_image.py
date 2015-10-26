import sys
import os
import glob
import ctypes
from PyQt4 import QtCore
from PyQt4 import QtGui


class MyWindow(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.input_path = 'C:/Users/Johns Lenovo/Pictures'
        newi = self.create_dir_table()
        return

    def create_dir_table(self):
        picture_type_list = ['*.png', '*.jpg', '*.gif', '*.bmp']
        self.pics_in_dir = []
        self.entry_count = 0
        for pic_type in picture_type_list:
            tl = glob.glob(self.input_path + '/' + pic_type)
            for inst in tl:
                filename = inst
                # filename = os.path.basename(inst)
                # creation_time = self.get_creation_times(filename)
                self.pics_in_dir.append([filename])
                self.entry_count += 1
        self.pics_in_dir = sorted(self.pics_in_dir, key=lambda x: x[0])
        for pics in self.pics_in_dir:
            self.load_picture_in_item(pics[0])
        return

    def load_picture_in_item(self, image_path,):
        print(image_path)
        item = QtGui.QTableWidgetItem()
        image = QtGui.QImage(image_path, "1")
        if not image.isNull():
            image_scaled = image.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
            pixmap = QtGui.QPixmap.fromImage(image_scaled)
            item.setData(QtCore.Qt.DecorationRole, pixmap)
        else:
            print("Image could not load")
            pixmap = QtGui.QPixmap(image_path)
            if pixmap.isNull():
                print("still")
            item.setData(QtCore.Qt.DecorationRole, pixmap)
        return item

if __name__ == '__main__':
    myappid = 'PhotoDrop.Beta.0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = MyWindow()
    sys.exit(app.exec_())
