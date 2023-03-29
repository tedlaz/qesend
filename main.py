# from PySide6 import QtWidgets
import os

from PyQt6 import QtWidgets
from PyQt6.QtCore import QStandardPaths

from extract_data import model_data
from model import Model
from ui_main import Ui_MainWindow
from utils import data2xlsx


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, ini):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.ini = ini
        self.setWindowTitle(self.ini.value("app_name", defaultValue="Δοκιμή"))
        self.etos_model = None
        self.trim_model = None
        self.mina_model = None
        self.anal_model = None
        self.make_connections()

    def make_connections(self):
        self.actionopen.triggered.connect(self.open)
        self.btn_csv_etos.clicked.connect(self.etos2csv)
        self.btn_csv_trimino.clicked.connect(self.trimino2csv)
        self.btn_csv_minas.clicked.connect(self.minas2csv)
        self.btn_csv_anal.clicked.connect(self.anal2csv)

    def save_file_dialog(self, default_file_name):
        desktop = QStandardPaths.StandardLocation.DesktopLocation
        wde = QStandardPaths.writableLocation(desktop)
        npath = os.path.join(wde, default_file_name)
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Αποθήκευση", npath, "Excel Files (*.xlsx)"
        )
        return filename

    def get_ini_sep_enc(self):
        separator = self.ini.value("csv_separator", defaultValue=",")
        encoding = self.ini.value("csv_encoding", defaultValue="utf-8")
        return separator, encoding

    def etos2csv(self):
        fname = self.save_file_dialog("etos.xlsx")
        if fname:
            data2xlsx(self.etos_model.mdata, fname)

    def trimino2csv(self):
        fname = self.save_file_dialog("trimino.xlsx")
        if fname:
            data2xlsx(self.trim_model.mdata, fname)

    def minas2csv(self):
        fname = self.save_file_dialog("minas.xlsx")
        if fname:
            data2xlsx(self.mina_model.mdata, fname)

    def anal2csv(self):
        fname = self.save_file_dialog("analytika.xlsx")
        if fname:
            data2xlsx(self.anal_model.mdata, fname)

    def open(self):
        # fnam, _ = qw.QFileDialog.getOpenFileName(self, "Open", self.fnam, "")
        # inif = INI.value('isozygio_file', defaultValue='')
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open", "", "*.html")
        if file_name:
            self.init_data(file_name)

    def init_data(self, htmlfile):
        detos, dtrim, dmina, anal = model_data(htmlfile)

        self.etos_model = Model(detos)
        self.trim_model = Model(dtrim)
        self.mina_model = Model(dmina)
        self.anal_model = Model(anal)

        self.table_etos.setModel(self.etos_model)
        self.table_trimino.setModel(self.trim_model)
        self.table_minas.setModel(self.mina_model)
        self.table_anal.setModel(self.anal_model)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        prefix = "file:///"
        postfix = ".html"
        dropped_txt = event.mimeData().text()
        if dropped_txt.startswith(prefix) and dropped_txt.endswith(postfix):
            fpath = dropped_txt.replace(prefix, "")
            self.init_data(fpath)
