from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic  # disable for py2exe
# import DBWindowUI  # enable for py2exe
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import urllib
import os
import datetime
import pyodbc  # needed for py2exe
import kustomWidgets


class DataBaseWindow(QtGui.QWidget):  # disable for py2exe
    # class DataBaseWindow(QtGui.QWidget, DBWindowUI.Ui_Form):  # enable for py2exe

    def __init__(self, parent):
        super().__init__()
        uic.loadUi('DBWindow.ui', self)  # disable for py2exe
        # self.setupUi(self)  # enable for py2exe
        self.settings = QtCore.QSettings('DBsettings.ini', QtCore.QSettings.IniFormat)
        self.parent = parent
        self.define_comboboxes()
        self.load_settings()
        self.ok_pushButton.clicked.connect(self.ok_pressed)
        self.cancel_pushButton.clicked.connect(self.cancel_pressed)
        self.use_db_checkBox.clicked.connect(self.db_checked)
        self.windows_auth_checkBox.clicked.connect(self.grey_out_settings)
        self.use_wsi_checkBox.clicked.connect(self.wsi_checked)
        self.wsi_browse_pushButton.clicked.connect(self.browse_directory)
        self.set_conn_type()

    def show_window(self):
        self.grey_out_settings()
        self.show()

    def define_comboboxes(self):
        suffix = "_comboBox"
        self.combo_list = [
                'server_name',
                'db_name',
                'login',
                'password',
                'wsi_dir']
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
        self.settings.setValue('use_wsi_checkBox', str(self.use_wsi_checkBox.checkState()))

    def load_settings(self):
        cd = self.combo_dict
        for cbox in cd.keys():
            cbox_obj = self.combo_obj_dict[cbox]
            if self.settings.value((cd[cbox]), []):
                cbox_obj.insertItems(0, self.settings.value((cd[cbox]), []))
        self.use_db_checkBox.setCheckState(int(self.settings.value('use_db_checkBox', QtCore.Qt.Unchecked)))
        self.windows_auth_checkBox.setCheckState(int(self.settings.value('windows_auth_checkBox', QtCore.Qt.Unchecked)))
        self.use_wsi_checkBox.setCheckState(int(self.settings.value('use_wsi_checkBox', QtCore.Qt.Unchecked)))

    def set_value_dict(self):
        for item in self.combo_list:
            self.value_dict[item] = getattr(getattr(self, self.combo_dict[item]), 'currentText')()

    def init_db_conn(self):
        self.set_value_dict()
        cs1 = "Driver={SQL Server Native Client 11.0}; Server=" + self.value_dict['server_name'] + ";"
        cs2 = " Database=" + self.value_dict['db_name'] + ";"
        if self.windows_auth_checkBox.isChecked():
            cs3 = "trusted_connection=yes;"
        else:
            uid = " UID=" + str(self.value_dict['login']) + ";"
            cs3 = uid + " PWD=" + str(self.value_dict['password']) + ";"
        conn_string = cs1 + cs2 + cs3
        self.parent.run_db_conn.set_conn_string(conn_string)
        self.parent.run_db_conn.connection_from_runnable()

    def browse_directory(self):
        new_directory_path = QtGui.QFileDialog.getExistingDirectory(None, '', self.wsi_dir_comboBox.currentText())
        # check directory here
        self.wsi_dir_comboBox.combobox_tidy(new_directory_path)

    def grey_out_settings(self):
        self.db_info_groupBox.setEnabled(self.use_db_checkBox.isChecked())
        self.uid_groupBox.setEnabled(not self.windows_auth_checkBox.isChecked())
        self.wsi_frame.setEnabled(self.use_wsi_checkBox.isChecked())

    def wsi_checked(self):
        if self.use_wsi_checkBox.isChecked():
            self.use_db_checkBox.setCheckState(QtCore.Qt.Unchecked)
        self.grey_out_settings()
        self.set_conn_type()

    def db_checked(self):
        if self.use_db_checkBox.isChecked():
            self.use_wsi_checkBox.setCheckState(QtCore.Qt.Unchecked)
        self.grey_out_settings()
        self.set_conn_type()

    def set_conn_type(self):
        if self.use_db_checkBox.isChecked():
            self.parent.run_db_conn = db_conn(self.parent)
            self.db_type = 'sql'
        elif self.use_wsi_checkBox.isChecked():
            self.set_value_dict()
            self.parent.run_db_conn = dir_db(self.parent, self.value_dict['wsi_dir'])
            self.db_type = 'dir'
        else:
            self.parent.run_db_conn = none_class()
            self.db_type = None

    def ok_pressed(self):
        for cbox_obj in self.combo_obj_dict:
            cur_line = self.combo_obj_dict[cbox_obj].currentText()
            self.combo_obj_dict[cbox_obj].combobox_tidy(cur_line)
        self.save_settings()
        self.hide()
        self.set_connection()

    def set_connection(self):
        self.set_conn_type()
        self.parent.pd_last_run_pushButton.setEnabled(self.parent.run_db_conn.status)
        if self.db_type == 'sql':
            self.init_db_conn()

    def cancel_pressed(self):
        self.load_settings()
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

    def set_conn_string(self, conn_string):
        self.thread_pool = QtCore.QThreadPool()
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
        run_number = last_run.Run_Number
        return run_number

    def get_run_time_dict(self):
        if self.status:
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
        except pyodbc.Error:
            self.signal.emit(self.signal.se_signal, False, None, None)
            print('SQL connection failure: pyodbc error')


class dir_db(object):

    def __init__(self, parent, path):
        self.parent = parent
        self.status = False
        data_string = '\\Data'
        if path.find(data_string) < 1:
            self.data_path = path + data_string + '\\'
        else:
            self.data_path = path
        self.get_run_time_dict()
        if len(self.parent.run_times) > 0:
            self.status = True

    def get_dir_list(self):
        try:
            self.list_of_runs = os.listdir(self.data_path)
        except:
            print('Directory not found')
            self.list_of_runs = []

    def get_run_time_dict(self):
        self.get_dir_list()
        self.parent.run_time_dict = {}
        self.parent.run_times = []
        for run in self.list_of_runs:
            if os.path.isdir(self.data_path + '\\' + run) is False:
                continue
            try:
                last_dash = run.rfind('_')
                if last_dash < 0 or last_dash < (len(run) - 8):
                    continue
                time_str = run[:last_dash]
                run_number = kustomWidgets.zeronater(int(run[run.rfind('_')+4:]), 3)
                # start_time = time.strptime(time_str, "%y%m%d_%H%M%S")
                start_time = datetime.datetime.strptime(time_str, "%y%m%d_%H%M%S")
                # self.parent.run_times.append(row.Run_endtime)
                self.parent.run_times.append(start_time)
                self.parent.run_time_dict[start_time] = 'pre-R' + str(run_number)
                # self.parent.run_time_dict[row.Run_endtime] = 'mid-R' + str(row.Run_Number)
            except:
                pass
        self.parent.run_times = sorted(self.parent.run_times, reverse=True)

    def last_run(self):
        self.get_run_time_dict()
        return self.parent.run_time_dict[self.parent.run_times[0]][5:]


class none_class(object):

    def __init__(self):
        self.status = False
