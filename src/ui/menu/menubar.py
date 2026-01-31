from PySide6 import QtWidgets
import ui.menu.menubar_utils as menubar_utils

class MenuBarWidget(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Init menus
        self.file_menu = self.addMenu("File")
        self.database_menu = self.addMenu("Database")
        self.setting_menu = self.addMenu("Setting")
        self.help_menu = self.addMenu("Help")
        self.about_menu = self.addMenu("About")

        # Add actions to File menu
        self.file_exit_action = self.file_menu.addAction("Exit")
        self.file_exit_action.triggered.connect(menubar_utils.on_file_exit)

        # Add actions to Index menu
        self.database_action = self.database_menu.addAction("Manage Databases")
        self.database_action.triggered.connect(menubar_utils.on_database_clicked)

        # Add action to Setting menu
        self.setting_action = self.setting_menu.addAction("Manage Settings")
        self.setting_action.triggered.connect(menubar_utils.on_setting_clicked)