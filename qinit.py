import os
import sys

# from PySide6.QtCore import QSettings
from PyQt6.QtCore import QSettings

INIFILE = "qesend.ini"

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    app_path = sys.executable
    frozen_dir_name = os.path.dirname(app_path)
    # YOUTUBE_DL_EXE_PATH = os.path.join(frozen_dir_name, 'youtube-dl.exe')
    INI_PATH = os.path.join(frozen_dir_name, INIFILE)
else:
    app_path = os.path.dirname(__file__)
    # YOUTUBE_DL_EXE_PATH = os.path.join(app_path, 'external', 'youtube-dl.exe')
    INI_PATH = os.path.join(app_path, INIFILE)

initial_ini = """[General]
save_path=
app_name=esend data viewer
csv_encoding=WINDOWS-1253
csv_separator=";"
"""

if not os.path.isfile(INI_PATH):
    with open(INI_PATH, "w", encoding="utf8") as fil:
        fil.write(initial_ini)

INI = QSettings(INIFILE, QSettings.Format.IniFormat)


def ini2dic(mainkey):
    """
    returns dictionary: {keyval1: [a1, a2, ...], keyval2: [b1, ..]}
    """
    fdict = {}
    INI.beginGroup(mainkey)
    for key in INI.allKeys():
        fdict[key] = INI.value(key).split()
    INI.endGroup()
    return fdict


def ini2dic_int_tuple(mainkey):
    """
    returns dictionary: {keyval1: [a1, a2, ...], keyval2: [b1, ..]}
    """
    fdict = {}
    INI.beginGroup(mainkey)
    for key in INI.allKeys():
        fdict[key] = tuple([int(i) for i in INI.value(key).split()])
    INI.endGroup()
    return fdict


# typoi = ini2dic('typoi')
# output = ini2dic('output')
# TPROCESS_INI = ini2dic('tprocess')
# videoformat = INI.value('videoformat').split()

# VIDEOSIZES = ini2dic_int_tuple('Videosizes')
