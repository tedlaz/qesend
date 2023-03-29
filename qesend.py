from PyQt6 import QtWidgets

from main import MainWindow
from qinit import INI

# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
app = QtWidgets.QApplication([])
# app.setOrganizationName("TedLazaros")
# app.setOrganizationDomain("Tedlaz")
# app.setApplicationName("qesend")
# app.setWindowIcon(QtGui.QIcon(":img/images/homeacc.svg"))
window = MainWindow(INI)
window.show()
app.exec()
