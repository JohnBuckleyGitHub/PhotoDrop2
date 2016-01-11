from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic  # disable for py2exe
# import DBWindowUI  # enable for py2exe
import sqlalchemy

import sqlalchemy.orm
import sqlalchemy.ext.automap
import urllib


class DataBaseWindow(QtGui.QWidget):  # disable for py2exe
    # class DataBaseWindow(QtGui.QWidget, DBWindowUI.Ui_Form):  # enable for py2exe

    def __init__(self, parent):
        super().__init__()
        uic.loadUi('DBWindow.ui', self)  # disable for py2exe
        # self.setupUi(self)  # enable for py2exe
        self.settings = QtCore.QSettings('DBsettings.ini', QtCore.QSettings.IniFormat)
        self.parent = parent
        # print('1st parent' + str(parent))
        self.define_comboboxes()
        self.load_settings()
        self.ok_pushButton.clicked.connect(self.ok_pressed)
        self.cancel_pushButton.clicked.connect(self.cancel_pressed)
        self.use_db_checkBox.clicked.connect(self.grey_out_settings)
        self.windows_auth_checkBox.clicked.connect(self.grey_out_settings)
        self.parent.run_db_conn = db_conn(self.parent)

    def show_window(self):
        self.grey_out_settings()
        self.show()

    def define_comboboxes(self):
        suffix = "_comboBox"
        self.combo_list = [
                'server_name',
                'db_name',
                'login',
                'password']
        self.combo_dict = {}
        self.combo_obj_dict = {}
        for item in self.combo_list:
            self.combo_dict[item] = item + suffix
            self.combo_obj_dict[item] = getattr(self, self.combo_dict[item])
            getattr(self.combo_obj_dict[item], 'setMaxCount')(5)
            pre_connect = getattr(self.combo_obj_dict[item], 'currentIndexChanged')
            setattr(self, item + '_change', self.cbox_change(self, item))
            funco = getattr(self, item + '_change')
            getattr(pre_connect, 'connect')(funco.line_change)
        self.value_dict = {}

    def save_settings(self):
        cd = self.combo_dict
        for cbox in cd.keys():
            cbox_obj = self.combo_obj_dict[cbox]
            cbox_items = list(cbox_obj.itemText(i) for i in range(cbox_obj.count()))
            self.settings.setValue(cd[cbox], cbox_items)
        self.settings.setValue('use_db_checkBox', str(self.use_db_checkBox.checkState()))
        self.settings.setValue('windows_auth_checkBox', str(self.windows_auth_checkBox.checkState()))

    def load_settings(self):
        cd = self.combo_dict
        for cbox in cd.keys():
            cbox_obj = self.combo_obj_dict[cbox]
            if self.settings.value((cd[cbox]), []):
                cbox_obj.insertItems(0, self.settings.value((cd[cbox]), []))
        self.use_db_checkBox.setCheckState(int(self.settings.value('use_db_checkBox', QtCore.Qt.Unchecked)))
        self.windows_auth_checkBox.setCheckState(int(self.settings.value('windows_auth_checkBox', QtCore.Qt.Unchecked)))

    def set_value_dict(self):
        for item in self.combo_list:
            self.value_dict[item] = getattr(getattr(self, self.combo_dict[item]), 'currentText')()

    def init_connection(self):
        self.set_value_dict()
        cs1 = "Driver={SQL Server};Server=" + self.value_dict['server_name'] + ";"
        cs2 = "Database=" + self.value_dict['db_name'] + ";"
        if self.windows_auth_checkBox.isChecked():
            cs3 = "trusted_connection=yes;"
        else:
            uid = "User Id=" + str(self.value_dict['login']) + ";"
            cs3 = uid + "Password=" + str(self.value_dict['password']) + ";"
        conn_string = cs1 + cs2 + cs3
        self.parent.run_db_conn.set_conn_string(conn_string)
        self.parent.run_db_conn.connection_from_runnable()

    def grey_out_settings(self):
        self.db_info_groupBox.setEnabled(self.use_db_checkBox.isChecked())
        self.uid_groupBox.setEnabled(not self.windows_auth_checkBox.isChecked())

    def ok_pressed(self):
        for cbox_obj in self.combo_obj_dict:
            cur_line = self.combo_obj_dict[cbox_obj].currentText()
            self.combo_obj_dict[cbox_obj].combobox_tidy(cur_line)
        # self.init_connection()
        self.save_settings()
        self.hide()
        self.parent.pd_last_run_pushButton.setEnabled(self.parent.run_db_conn.status)
        self.init_connection()

    def cancel_pressed(self):
        self.hide()

    class cbox_change(object):

        def __init__(self, parent, cbox_name):
            self.parent = parent
            self.name = cbox_name

        def line_change(self, event):
            self.parent.combo_obj_dict[self.name].combobox_sort()


class db_conn(QtCore.QObject):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.status = False
        self.thread_pool = QtCore.QThreadPool()

    def set_conn_string(self, conn_string):
        self.conn_string = conn_string
        pconn = urllib.parse.quote_plus(self.conn_string)
        self.engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % pconn)
        self.status = False

    def connection_from_runnable(self):
        worker = ConnectionRunnable(self.engine)
        self.connect(worker.signal, worker.signal.se_signal, self.connection_status)
        self.thread_pool.start(worker)

    def connection_status(self, status, session, runs):
        if status:
            self.status = True
            self.session = session
            self.runs = runs
        else:
            self.status = False
            return
        self.parent.pd_last_run_pushButton.setEnabled(self.parent.run_db_conn.status)
        self.get_run_time_dict()

    def last_run(self):
        last_run = self.session.query(self.runs).order_by(self.runs.Run_Number.desc()).first()
        return last_run

    def get_run_time_dict(self):
        self.parent.run_time_dict = {}
        self.parent.run_times = []
        for row in self.session.query(self.runs).order_by(self.runs.Run_Number.desc()).all():
            self.parent.run_times.append(row.Run_endtime)
            self.parent.run_times.append(row.Run_starttime)
            self.parent.run_time_dict[row.Run_starttime] = 'pre-R' + str(row.Run_Number)
            self.parent.run_time_dict[row.Run_endtime] = 'mid-R' + str(row.Run_Number)


class SignalEmitter(QtCore.QObject):
    #  Needed because QRunnable does not emit a signal

    def __init__(self):
        super().__init__()
        self.se_signal = QtCore.SIGNAL("connection_signal")


class ConnectionRunnable(QtCore.QRunnable):

    def __init__(self, engine):
        super().__init__()
        self.signal = SignalEmitter()
        self.engine = engine

    def run(self):
        # establishes connection
        try:
            self.engine.connect()
            session = sqlalchemy.orm.Session(self.engine)
            base = sqlalchemy.ext.automap.automap_base()
            base.prepare(self.engine, reflect=True)
            runs = base.classes.Runs
            self.signal.emit(self.signal.se_signal, True, session, runs)
        except sqlalchemy.exc.ProgrammingError:
            self.signal.emit(self.signal.se_signal, False, None, None)
            print('SQL connection failure: ProgrammingError')
        except sqlalchemy.exc.DBAPIError:
            self.signal.emit(self.signal.se_signal, False, None, None)
            print('SQL connection failure: DBAPIError')
