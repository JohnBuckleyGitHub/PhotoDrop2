from PyQt4 import QtGui
from PyQt4 import QtCore
# from PyQt4 import uic
import DBWindowUI


class DataBaseWindow(QtGui.QWidget, DBWindowUI.Ui_Form):

    def __init__(self):
        super().__init__()
        # uic.loadUi('DBWindow.ui', self)
        self.setupUi(self)
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

    def grey_out_settings(self):
        if self.use_db_checkBox.isChecked():
            self.db_info_groupBox.setEnabled(True)
        else:
            self.db_info_groupBox.setEnabled(False)

    def use_windows_auth(self):
        print(self.windows_auth_checkBox.isChecked())

    def ok_pressed(self):
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