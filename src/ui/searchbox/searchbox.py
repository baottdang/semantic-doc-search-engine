from pathlib import Path
from PySide6 import QtWidgets
from resources.strings.string_resource import filters
from PySide6.QtCore import Slot, Qt
from services.database import database as db
from services.threads.taskqueue import get_task_queue_instance
from ui.searchbox import searchbox_utils as utils
import services.index.index_construct_signal as construct_signal
import os

class FileSearchBoxWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a search bar component
        self.searchbox = QtWidgets.QLineEdit(self)
        self.searchbox.setPlaceholderText("Enter file directory or browse")
        self.searchbox.textChanged.connect(self.on_query_text_change)
        # Create a browse button
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.on_browse_clicked)
        # Screenshot button
        self.screenshot_button = QtWidgets.QPushButton("Screenshot")
        # Layout setup
        self.layout = QtWidgets.QHBoxLayout()

        # Apply layout to file searchbox
        self.layout.addWidget(self.searchbox)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.screenshot_button)
        self.setLayout(self.layout)

    @Slot()
    def on_browse_clicked(self):
        # Open a file dialog to select a file
        self.file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", filters)
        if self.file_name:
            file_path = Path(self.file_name)
            self.searchbox.setText(str(file_path))

    @Slot()
    def on_query_text_change(self):
        path = self.searchbox.text()
        tq = get_task_queue_instance()
        if os.path.isfile(path):
            tq.submit(lambda : utils.submit_query_display(path))
        else:
            tq.submit(utils.submit_query_clear)

    def get_file_path(self):
        return self.searchbox.text()

class DatabaseSearchBoxWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Label
        self.label = QtWidgets.QLabel("From Database ")
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.adjustSize()

        # Create a drop down component
        self.database = db.get_main_database_instance()
        self.folderbox = QtWidgets.QComboBox()
        self.folderbox.addItems([path for path in self.database.get_indexed_database_paths() if os.path.exists(path)])

        # Signals
        self.construct_signal = construct_signal.get_construct_signal_instance()
        self.construct_signal.construct_complete_signal.connect(self.update_database_selection)

        # Layout setup
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        
        # Apply layout to database searchbox
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.folderbox)
        self.setLayout(self.layout)

    def get_selected_database(self):
        return self.folderbox.currentText()
    
    def update_database_selection(self):
        self.folderbox.clear()
        self.folderbox.addItems([path for path in self.database.get_indexed_database_paths() if os.path.exists(path)])

class SearchBoxWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create search components
        self.file_searchbox = FileSearchBoxWidget(self)
        self.database_searchbox = DatabaseSearchBoxWidget(self)
        self.search_button = QtWidgets.QPushButton(" Search ")
        self.search_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.search_button.clicked.connect(self.on_search_clicked)

        # Layout setup
        self.layout = QtWidgets.QVBoxLayout()

        # Apply layout to search components
        self.layout.addWidget(self.file_searchbox)
        self.layout.addWidget(self.database_searchbox)
        self.layout.addWidget(self.search_button, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)

    @Slot()
    def on_search_clicked(self):
        file_path = self.file_searchbox.get_file_path()
        database_path = self.database_searchbox.get_selected_database()
        if os.path.isfile(file_path) and os.path.isdir(database_path):
            tq = get_task_queue_instance()
            future = tq.submit(lambda: utils.query(file_path, database_path))
            future.add_done_callback(utils.query_done)
        

        
