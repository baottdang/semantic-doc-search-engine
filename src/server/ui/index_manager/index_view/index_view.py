from PySide6 import QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Slot
from services.db_interface.db_manager import get_db_manager
from services.index.index_construct_signal import get_construct_signal_instance
from ui.index_manager.index_view.listview import CustomListView

class IndexView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Database
        self.db_manager = get_db_manager()

        # Tree View to display the metadata
        self.view = CustomListView()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Database Name", "Database Path", "Index Model Used", "Date Indexed"])

        self.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.view.setModel(self.model)

        self.load_indices()

        # Signal
        self.index_construct_signal_instance = get_construct_signal_instance()
        self.index_construct_signal_instance.construct_complete_signal.connect(self.append_table)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    @Slot()
    def append_table(self, table):
        name, path, index_model, date_indexed = table.get_info()
        self.model.appendRow([QStandardItem(name), QStandardItem(path), QStandardItem(index_model), QStandardItem(date_indexed)])

    def load_indices(self):
        self.model.removeRows(0, self.model.rowCount()) # Clear old data
        for table in self.db_manager.tables.values():
            name, path, index_model, date_indexed = table.get_info()
            self.model.appendRow([QStandardItem(name), QStandardItem(path), QStandardItem(index_model), QStandardItem(date_indexed)])

        