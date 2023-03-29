# from PySide6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtCore import QAbstractTableModel, Qt

from model_data import ModelData
from utils import grnum

QTALIGN = {
    1: int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
    2: int(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter),
    3: int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter),
}

QTDISPLAY = {
    0: str,
    1: grnum,
}


class Model(QAbstractTableModel):
    def __init__(self, model_data: ModelData, parent=None):
        super().__init__(parent)
        self.mdata = model_data

    def rowCount(self, parent):
        return len(self.mdata.rows)

    def columnCount(self, parent):
        return len(self.mdata.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.mdata.headers[section]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            func = QTDISPLAY.get(self.mdata.isgrnum[index.column()], 0)
            return func(self.mdata.rows[index.row()][index.column()])

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return QTALIGN.get(self.mdata.aligns[index.column()], 1)
