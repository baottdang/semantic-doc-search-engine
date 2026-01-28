from PySide6.QtCore import Slot
from PySide6 import QtWidgets
from ui.index_setup.index_setup import IndexSetupWidget
from ui.setting.setting_window import SettingWindow

# Store single instances of windows to be reused later
index_window = None
setting_window = None

@Slot()
def on_file_exit():
    QtWidgets.QApplication.instance().quit()

@Slot()
def on_add_index():
    global index_window
    if index_window is None:
        index_window = IndexSetupWidget()
    index_window.show()

@Slot()
def on_setting_clicked():
    global setting_window
    if setting_window is None:
        setting_window = SettingWindow()
    setting_window.show()