from PySide6.QtCore import Qt
from PySide6 import QtWidgets
from ui.menu.menubar import MenuBarWidget
from ui.searchbox.searchbox import SearchBoxWidget, SearchBoxWidget
from ui.sidebar.sidebar import SidebarWidget
from ui.status_bar.status_bar import StatusBar
from ui.error.error_signal import get_error_signal_instance
from ui.main_area.main_area import MainArea
import resources.strings.string_resource

class BackgroundWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(resources.strings.string_resource.app_name)
        self.setMinimumSize(800, 600)

        # Add menu bar
        self.menu_bar = MenuBarWidget(self)
        self.setMenuBar(self.menu_bar)

        # Create a searchbox
        self.search_box = SearchBoxWidget(self)

        # Signals
        self.error_instance = get_error_signal_instance()
        self.error_instance.error_signal.connect(self.display_error)

        # Set toolbar widget
        self.tool_bar = QtWidgets.QToolBar("Search Box", self)
        self.tool_bar.setMovable(False)
        self.tool_bar.addWidget(self.search_box)
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)

        # Set sidebar widget
        self.sidebar = QtWidgets.QDockWidget("Properties", self)
        self.sidebar.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.sidebar.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable)
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(600)
        self.sidebar_widget = SidebarWidget(self)
        self.sidebar.setWidget(self.sidebar_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)

        # Set status bar
        self.status_bar = self.setStatusBar(StatusBar())

        # Set central widget
        self.central_widget = MainArea()
        self.setCentralWidget(self.central_widget)

    def get_status_bar(self):
        return self.status_bar
    
    def display_error(self, error_name, error_msg):
        critical = QtWidgets.QMessageBox().critical(self, error_name, error_msg)