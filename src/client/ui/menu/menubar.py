from PySide6 import QtWidgets
import ui.menu.menubar_utils as menubar_utils

class MenuBarWidget(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Init menus
        self.file_menu = self.addMenu("File")

        # Add actions to File menu
        self.file_exit_action = self.file_menu.addAction("Exit")
        self.file_exit_action.triggered.connect(menubar_utils.on_file_exit)
