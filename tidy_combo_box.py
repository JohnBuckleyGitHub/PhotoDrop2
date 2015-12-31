from PyQt4 import QtGui


class TidyComboBox(QtGui.QComboBox):

    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)
        # super().__init__(parent)
        self.max_items = None

    def combobox_sort(self):
        # cb = self.parent
        self.blockSignals(True)
        current_index = self.currentIndex()
        current_text = self.currentText()
        self.removeItem(current_index)
        self.insertItem(0, current_text)
        self.setCurrentIndex(0)
        self.blockSignals(False)

    def combobox_tidy(self, line):
        if line in self.get_combo_items():
            position = self.get_combo_items().index(line)
            self.removeItem(position)
        self.insertItem(0, line)
        self.setCurrentIndex(0)
        if self.max_items:
            item_count = self.count()
            if item_count > self.max_items:
                for i in range(self.max_items, item_count):
                    self.parent.removeItem(i)

    def get_combo_items(self):
        return [self.itemText(i) for i in range(self.count())]
