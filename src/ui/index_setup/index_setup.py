from pathlib import Path
from PySide6.QtCore import Slot
from PySide6 import QtWidgets
from ui.index_setup.index_setup_utils import is_child_of_indexed, is_indexed, done_setup
from src.services.index.index_construct import construct_index
from services.threads import taskqueue as tq
import ui.index_setup.index_setup_signal as signal
import services.index.index_construct_signal as construct_signal

class IndexSetupWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add new database")
        self.setFixedWidth(400)
        self.setFixedHeight(150)

        # Components
        self.from_label = QtWidgets.QLabel("Database: ")
        self.path_field = QtWidgets.QLineEdit(self)
        self.path_field.setPlaceholderText("Enter path to database")
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.on_browse_clicked)
        self.add_database_button = QtWidgets.QPushButton("Add This Database")
        self.add_database_button.clicked.connect(self.on_add_database_clicked)

        # Signals
        self.signal = signal.get_index_signal_instance()
        self.construct_signal = construct_signal.get_construct_signal_instance()
        self.construct_signal.construct_complete_signal.connect(self.complete_add_index)
        self.construct_signal.construct_error_signal.connect(self.error_add_index)
        
        # Layout setup
        self.browser_layout = QtWidgets.QHBoxLayout()
        self.browser_layout.addWidget(self.from_label)
        self.browser_layout.addWidget(self.path_field)
        self.browser_layout.addWidget(self.browse_button)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.browser_layout)
        self.layout.addWidget(self.add_database_button)
        self.setLayout(self.layout)
        
    @Slot()
    def on_browse_clicked(self):
        # Open a file dialog to select a database file
        folder_name= QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_name:
            folder_path = Path(folder_name)
            self.path_field.setText(str(folder_path))

    @Slot()
    def on_add_database_clicked(self):
        if is_child_of_indexed(self.get_database_path()): # Check if this folder is already a subdir of an indexed database
            display_warning = QtWidgets.QMessageBox().warning(self, "Notice", "A parent database of this folder is already indexed!")
        elif is_indexed(self.get_database_path()): # Check if this folder is already indexed
            display_warning = QtWidgets.QMessageBox().warning(self, "Notice", "Database is already indexed!")
        else:
            taskqueue = tq.get_task_queue_instance() # Background thread handles the construction of index
            future = taskqueue.submit(construct_index, self.get_database_path())
            self.start_add_index()
            future.add_done_callback(done_setup)

    def start_add_index(self):
        self.setEnabled(False)
        self.signal.index_start_signal.emit(self.get_database_path())

    @Slot()
    def complete_add_index(self, path, index_name):
        self.setEnabled(True)
        self.signal.index_complete_signal.emit(path, index_name)

    @Slot()
    def error_add_index(self, database_name):
        self.setEnabled(True)
        self.signal.index_error_signal.emit(database_name)

    def get_database_path(self):
        return self.path_field.text()
    