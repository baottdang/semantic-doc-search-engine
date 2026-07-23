from PySide6.QtCore import Slot
from PySide6 import QtWidgets
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

# Store single instances of windows to be reused later
index_window = None
setting_window = None

@Slot()
def on_file_exit():
    QtWidgets.QApplication.instance().quit()