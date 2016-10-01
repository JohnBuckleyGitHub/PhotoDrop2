from PyQt4 import QtGui
#  Version 1.1
#  Update is version control


class TidyComboBox(QtGui.QComboBox):

    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)

    def combobox_sort(self):
        self.blockSignals(True)
        current_index = self.currentIndex()
        current_text = self.currentText()
        self.removeItem(current_index)
        self.insertItem(0, current_text)
        self.setCurrentIndex(0)
        self.blockSignals(False)

    def combobox_tidy(self, line):
        self.blockSignals(True)
        if line in self.get_combo_items():
            position = self.get_combo_items().index(line)
            self.removeItem(position)
        self.insertItem(0, line)
        self.setCurrentIndex(0)
        self.blockSignals(False)

    def get_combo_items(self):
        return [self.itemText(i) for i in range(self.count())]
