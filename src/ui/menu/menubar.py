from PySide6 import QtWidgets
import ui.menu.menubar_utils as menubar_utils

class MenuBarWidget(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Init menus
        self.file_menu = self.addMenu("File")
        self.index_menu = self.addMenu("Index")
        self.help_menu = self.addMenu("Help")
        self.about_menu = self.addMenu("About")

        # Add actions to File menu
        self.file_exit_action = self.file_menu.addAction("Exit")
        self.file_exit_action.triggered.connect(menubar_utils.on_file_exit)

        # Add actions to Index menu
        self.index_add_action = self.index_menu.addAction("Add Index")
        self.index_delete_action = self.index_menu.addAction("Delete Index")
        self.index_add_action.triggered.connect(menubar_utils.on_add_index)