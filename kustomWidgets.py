from PyQt4 import QtCore
from PyQt4 import QtGui
# import sys
import math
# sys.path.insert(0, 'C:/Python Files/pythonlibs')
# import kustomDBtools


    ###############################################################################
    #Contains status_label_class, qsettings_handler, and brushstyle
    ###############################################################################


    ##############################################################################
    # Status bar
    #
    # Requires a scrolled window with an area called status_label
    # Best if inherited upon window declaration class MyWindow(QtGui.QMainWindow,  kustomWidgets.status_label_class, ...)
    #
    ##############################################################################

class status_label_class(object):
    def __init__(self):
        pass
        # self.status_label = window.status_label

    def statusbar_add(self, new_text, special_text=False):
        html_ins = ''
        if special_text is False:
            html_ins = special_text
        current_text = self.status_label.text()
        full_text = "<p><" + html_ins + ">" + new_text + "</" + html_ins + "></p>" + current_text
        line_count = full_text.count('</p>')
        if line_count > 100:
            last_n = full_text.rfind('</p>')
            full_text = full_text[:last_n]
        self.status_label.setText(full_text)

    ##############################################################################
    # QSettings handling - save, default, delete
    #
    # Requires a scrolled window with an area called status_label
    # Initiated as a new object and window refers to the active window
    #
    ##############################################################################


class qsettings_handler(object):

    def __init__(self, window, prefix_name, default_setting_name):
        self.window = window
        self.view_settings_comboBox = window.view_settings_comboBox
        self.qsettings_prefix_name = prefix_name  # "DB Admin"
        self.qsettings_company = "JP Buckley Aerodynamics"
        self.qsettings_name = default_setting_name  # "column_view"
        self.qt_settings = QtCore.QSettings(self.qsettings_company, self.qsettings_name)

    def column_order_store(self):
        self.qt_settings.setValue(self.qsettings_name, self.window.DB_tableWidget.horizontalHeader().saveState())

    def load_view_settings(self):
        self.view_settings_comboBox.clear()
        db_obj = self.config_qsetting()
        saved_views = ['Current']
        actions = ['Save Current', 'Delete View']
        for entry in db_obj.entries:
            first_comma = entry['Full_Name'].find(",")
            new_view = entry['Full_Name'][first_comma+1:]
            saved_views.append(new_view)
        saved_views += actions
        self.view_settings_comboBox.addItems(saved_views)
        self.delete_view = False

    def change_view_settings(self):
        combo_box = self.view_settings_comboBox
        current_selection = combo_box.currentText()
        db_obj = self.config_qsetting()
        if not self.delete_view == True:
            if current_selection == 'Current':
                return
            elif current_selection == 'Save Current':
                all_box_items = [combo_box.itemText(i) for i in range(combo_box.count())]
                new_view_name = 'Save Current' # to keep while loop going
                while new_view_name in all_box_items:
                    new_view_name, ok_or_cancel = QtGui.QInputDialog.getText(self.window, 'New View Name','Enter a name for the new saved view:')
                    if new_view_name in all_box_items or new_view_name == '':
                        self.window.statusbar_add('View name ' + new_view_name + ' already exists')
                if ok_or_cancel == False:
                    self.load_view_settings()
                    self.window.statusbar_add("Save view exited")
                    return
                if new_view_name == "Default Replace":
                    new_view_name = "Default"
                insert_dict = {}
                insert_dict['Full_Name'] = self.qsettings_prefix_name + ',' + new_view_name
                insert_dict['Company'] = self.qsettings_company
                insert_dict['Qbyte_String'] = self.window.DB_tableWidget.horizontalHeader().saveState()
                statustext = db_obj.insert_row(insert_dict)
                if statustext:
                    self.window.statusbar_add(str(statustext))
                self.load_view_settings()
            elif current_selection == 'Delete View':
                self.delete_view = True
                self.window.statusbar_add("Delete view mode: Select a view to delete", special_text='b')
                return
            elif current_selection != 'Current' and current_selection != 'Save Current' and current_selection != 'Delete Current':
                db_obj.select_all()
                found = False
                for entry in db_obj.entries:
                    first_comma = entry['Full_Name'].find(",")
                    new_view = entry['Full_Name'][first_comma+1:]
                    if new_view == current_selection:
                        self.window.statusbar_add(current_selection + " view retrieved from config.db")
                        found = True
                        self.qt_settings.setValue(self.qsettings_name, entry['Qbyte_String'])
                        self.window.DB_tableWidget.horizontalHeader().restoreState(self.qt_settings.value(self.qsettings_name)) #reset columns
                if not found:
                    self.window.statusbar_add(current_selection + " not found in config.db, no change made.")
                self.load_view_settings()
                self.window.refresh_db_table()
        elif self.delete_view == True:
            undeletable = ['Current', 'Save Current', 'Delete View', 'Default']
            if current_selection not in undeletable:
                delete_box = QtGui.QMessageBox()
                delete_box.setText("Do you want to delete view " + current_selection)
                delete_box.setStandardButtons(delete_box.Ok | delete_box.Cancel)
                answer = delete_box.exec()
                if answer == 0x00000400: # 0x00000400 is OK see - http://qt-project.org/doc/qt-4.8/qmessagebox.html#StandardButton-enum
                    db_obj.remove_row('Full_Name', self.qsettings_prefix_name + ',' + current_selection)
                    self.window.statusbar_add(current_selection + " removed from config.db")
            self.delete_view = False
            self.window.statusbar_add("Delete view mode: exited", special_text='b')
            self.load_view_settings()

    def config_qsetting(self):
        db_name = "config.db"
        conn_string = db_name
        default_table = "Qsettings_External"
        select_default = ("WHERE Company='" + self.qsettings_company + "' AND Full_Name LIKE '" +
            self.qsettings_prefix_name + "%'")
        # config_db_obj = kustomDBtools.db_obj(conn_string, default_table, select_default)
        config_db_obj.select_all()
        return(config_db_obj)

    #######################################
    # brushsyle contains brushestyles with predefined colors
    #######################################


class brushstyle(object):

    def __init__(self):
        self.red = QtGui.QBrush(QtGui.QColor(255, 189, 189))
        self.red.setStyle(QtCore.Qt.SolidPattern)
        self.grey = QtGui.QBrush(QtGui.QColor(80, 80, 80))
        self.grey.setStyle(QtCore.Qt.SolidPattern)
        self.nobrush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.nobrush.setStyle(QtCore.Qt.SolidPattern)

    #######################################
    # Misc
    #######################################


def dir_clean(init_str):
    if init_str[-1:] != "/" and init_str[-1:] != "\\":
        return init_str + "/"
    return init_str


def zeronater(number, place_count):
    if number < 1:
        output_string = ''
        for i in range(place_count):
            output_string += '0'
        return output_string
    places = int(math.log(number)/math.log(10) + 1)
    output_string = str(int(number))
    for i in range(place_count - places):
        output_string = '0' + output_string
    return output_string
