from PySide6 import QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Slot, QModelIndex
from services.database.database import get_main_database_instance
from services.index.index_construct_signal import get_construct_signal_instance
from ui.index_manager.index_view.listview import CustomListView

class IndexView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Database
        self.db = get_main_database_instance()

        # Tree View to display the metadata
        self.view = CustomListView()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Database'])

        self.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.view.setModel(self.model)

        self.load_indices()

        self.view.clicked[QModelIndex].connect(self.entry_on_clicked)

        # Signal
        self.index_construct_signal_instance = get_construct_signal_instance()
        self.index_construct_signal_instance.construct_complete_signal.connect(self.append_index)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    @Slot()
    def append_index(self, folder_path, index_name):
        self.model.appendRow(QStandardItem(folder_path))

    def load_indices(self):
        self.model.removeRows(0, self.model.rowCount()) # Clear old data
        for index in self.db.get_indexed_database_paths():
            self.model.appendRow(QStandardItem(index))

        