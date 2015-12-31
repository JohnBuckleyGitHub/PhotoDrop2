from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic  # disable for py2exe
# import DBWindowUI  # enable for py2exe


class DataBaseWindow(QtGui.QWidget):  # disable for py2exe
    # class DataBaseWindow(QtGui.QWidget, DBWindowUI.Ui_Form):  # enable for py2exe

    def __init__(self):
        super().__init__()
        uic.loadUi('DBWindow.ui', self)  # disable for py2exe
        # self.setupUi(self)  # enable for py2exe
        self.settings = QtCore.QSettings('DBsettings.ini', QtCore.QSettings.IniFormat)
        self.define_comoboxes()
        self.load_settings()
        self.ok_pushButton.clicked.connect(self.ok_pressed)
        self.cancel_pushButton.clicked.connect(self.cancel_pressed)
        self.use_db_checkBox.clicked.connect(self.grey_out_settings)
        self.windows_auth_checkBox.clicked.connect(self.use_windows_auth)

    def show_window(self):
        self.grey_out_settings()
        self.show()

    def define_comoboxes(self):
        suffix = "_comboBox"
        self.combo_list = [
                'server_name',
                'db_name',
                'login',
                'password']
        self.combo_dict = {}
        for item in self.combo_list:
            self.combo_dict[item] = item + suffix
        self.value_dict = {}

    def save_settings(self):
        cd = self.combo_dict
        max_items = 5
        for cbox in cd.keys():
            cbox_obj = getattr(self, cd[cbox])
            cbox_items = list(cbox_obj.itemText(i) for i in range(cbox_obj.count()))
            cbox_items = cbox_items[:max_items]
            self.settings.setValue(cd[cbox], cbox_items)

    def load_settings(self):
        cd = self.combo_dict
        for cbox in cd.keys():
            cbox_obj = getattr(self, cd[cbox])
            if self.settings.value((cd[cbox]), []):
                cbox_obj.insertItems(0, self.settings.value((cd[cbox]), []))

    def set_value_dict(self):
        for item in self.combo_list:
            self.value_dict[item] = getattr(self, self.combo_dict[item] + '.currentText()')

    def create_conn_string(self):
        self.set_value_dict()
        server = getattr(self, self.combo_dict['server_name'] + '.currentText()')
        database = getattr(self, self.combo_dict['db_name'] + '.currentText()')
        print(server)
        print(database)
        cs1 = "Driver={SQL Server};Server=" + self.value_dict['server_name'] + ";"
        cs2 = "Database=" + self.value_dict['db_name'] + ";"
        if self.windows_auth_checkBox.isChecked():
            cs3 = "trusted_connection=yes;"
        else:
            uid = "User Id=" + str(self.value_dict['login']) + ";"
            cs3 = uid + "Password=" + str(self.value_dict['password']) + ";"
        self.conn_string = cs1 + cs2 + cs3
        print("conn_string")

    def grey_out_settings(self):
        if self.use_db_checkBox.isChecked():
            self.db_info_groupBox.setEnabled(True)
        else:
            self.db_info_groupBox.setEnabled(False)

    def use_windows_auth(self):
        print(self.windows_auth_checkBox.isChecked())

    def ok_pressed(self):
        self.create_conn_string()
        self.save_settings()
        self.hide()

    def cancel_pressed(self):
        self.hide()





# conn = "Driver={SQL Server};Server=DESKTOP-6E0R1GC;Database=ChevyIRL2013;trusted_connection=yes;"
# pconn = urllib.parse.quote_plus(conn)
# engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % pconn)
# engine.connect()

# session = sqlalchemy.orm.Session(engine)
# base = sqlalchemy.ext.automap.automap_base()
# base.prepare(engine, reflect=True)
# # metadata = sqlalchemy.Metadata()
# # metadata.reflect(engine, only=['Runs'])
# runs = base.classes.Runs
# last_run = session.query(runs).order_by(runs.Run_Number.desc()).first()