from PySide6.QtCore import Slot
from ui.index_setup.index_setup import IndexSetupWidget
from PySide6 import QtWidgets

index_window = None

@Slot()
def on_file_exit():
    QtWidgets.QApplication.instance().quit()

@Slot()
def on_add_index():
    global index_window
    if index_window is None:
        index_window = IndexSetupWidget()
    index_window.show()