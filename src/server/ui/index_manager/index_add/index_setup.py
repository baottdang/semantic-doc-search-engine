from pathlib import Path
from PySide6.QtCore import Slot
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from ui.index_manager.index_add.index_setup_utils import is_child_of_indexed, is_indexed
from services.index.index_construct import construct_index
from resources.strings.string_resource import icon_path
import services.index.index_construct_signal as construct_signal
import threading

class IndexSetupWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add new database")
        self.setFixedWidth(400)
        self.setFixedHeight(150)        
        self.setWindowIcon(QIcon(icon_path))

        # Components
        self.from_label = QtWidgets.QLabel("Database: ")
        self.path_field = QtWidgets.QLineEdit(self)
        self.path_field.setPlaceholderText("Enter path to database")
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.on_browse_clicked)
        self.add_database_button = QtWidgets.QPushButton("Add This Database")
        self.add_database_button.clicked.connect(self.on_add_database_clicked)

        # Signals
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
        f_path = self.get_database_path()
        if is_child_of_indexed(f_path): # Check if this folder is already a subdir of an indexed database
            QtWidgets.QMessageBox().warning(self, "Notice", "A parent database of this folder is already indexed!")
        elif is_indexed(f_path): # Check if this folder is already indexed
            QtWidgets.QMessageBox().warning(self, "Notice", "Database is already indexed!")
        else:
            index_construct_thread = threading.Thread(target=construct_index, args=(f_path,), daemon=True)
            index_construct_thread.start()
            self.start_add_index()

    def start_add_index(self):
        self.setEnabled(False)

    @Slot()
    def complete_add_index(self, table):
        QtWidgets.QMessageBox().information(self, "Indexing Completed Successfully!", f"Added {table.folder_path} as {table.table_name} to database")
        self.setEnabled(True)

    @Slot()
    def error_add_index(self, database_name, msg):
        QtWidgets.QMessageBox().critical(self, f"Something went wrong while adding {database_name}!", msg)
        self.setEnabled(True)

    def get_database_path(self):
        return self.path_field.text()
    