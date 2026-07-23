from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from ui.index_manager.index_add.index_setup import IndexSetupWidget
from ui.index_manager.index_view.index_view import IndexView
from resources.strings.string_resource import icon_path

class IndexManagerWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manage Databases")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.setWindowIcon(QIcon(icon_path))

        # Components
        self.listview = IndexView()

        self.add_index_button = QtWidgets.QPushButton("New database")
        self.add_index_button.clicked.connect(self.add_index_clicked)
        self.index_add_window = None

        # Layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.listview)
        self.layout.addWidget(self.add_index_button)

        self.setLayout(self.layout)

    @Slot()
    def add_index_clicked(self):
        if self.index_add_window is None:
            self.index_add_window = IndexSetupWidget()
        self.index_add_window.show()
