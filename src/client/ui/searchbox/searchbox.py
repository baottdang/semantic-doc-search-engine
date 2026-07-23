from PySide6 import QtWidgets
from resources.strings.string_resource import filters
from PySide6.QtCore import Slot, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut, QKeyEvent
from services.threads.taskqueue import get_task_queue_instance
from ui.searchbox import searchbox_utils as utils
from ui.screenshotcapture.screencapture import ScreenCapture
from ui.searchbox.searchbox_signal import get_searchbox_signal_instance
from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS
from services.client.client import get_client
from services.query.query_utils import QImageToCvMat
import os

class FileSearchBoxWidget(QtWidgets.QWidget):
    class CustomLineEdit(QtWidgets.QLineEdit):
        def keyPressEvent(self, event: QKeyEvent):
            if event == QKeySequence.Paste:  # Ctrl+V
                clipboard = QtWidgets.QApplication.clipboard()
                if clipboard.mimeData().hasImage():
                    self.parent().handle_paste_img()
                elif clipboard.mimeData().hasText():
                    text = clipboard.text()
                    self.insert(text)
            else:
                super().keyPressEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a search bar component
        self.searchbox = self.CustomLineEdit(self)
        self.searchbox.setPlaceholderText("Enter file directory or browse")
        self.searchbox.textEdited.connect(self.on_query_text_edited)
        self._use_image_query = False

        # Drag and drop, clipboard pasting
        self.dnd_bar = QtWidgets.QLabel(self)
        self.dnd_bar.setText("Drag and drop image here or paste from clipboard")
        self.dnd_bar.setStyleSheet("""
                border: 1px solid #333;
                border-radius: 10px;
                padding: 5px;
                background-color: #2A3545
            """)
        self.dnd_bar.setAlignment(Qt.AlignCenter)

        # Shortcut for pasting
        self.paste_shortcut = QShortcut(QKeySequence.Paste, self)
        self.paste_shortcut.activated.connect(self.handle_paste_img)
        self.paste_shortcut.setContext(Qt.ApplicationShortcut)

        # Create a browse button
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.on_browse_clicked)

        # Screenshot button
        self.screenshot_button = QtWidgets.QPushButton("Screenshot")
        self.screenshot_button.clicked.connect(self.on_screenshot_clicked)
        self.capture = None

        # Signal
        self.searchbox_signal_instance = get_searchbox_signal_instance()
        self.searchbox_signal_instance.capture_done_signal.connect(utils.submit_query_image_display) # Connect the screencapture's result to display

        # Layout setup
        self.searchbar_layout = QtWidgets.QVBoxLayout()
        self.layout = QtWidgets.QHBoxLayout()

        # Apply layout to file searchbox
        self.searchbar_layout.addWidget(self.searchbox)
        self.searchbar_layout.addWidget(self.dnd_bar)

        self.layout.addLayout(self.searchbar_layout)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.screenshot_button)
        self.setLayout(self.layout)

    @Slot()
    def clear_text_query(self):
        """
        Clear text in file searchbox
        
        """
        self.searchbox.setText("")

    @Slot()
    def handle_paste_img(self):
        clipboard = QtWidgets.QApplication.clipboard()
        if not clipboard.mimeData().hasImage():
            return
        else:
            self.capture = QImageToCvMat(clipboard.image())
            self._use_image_query = True 
            self.clear_text_query()
            utils.submit_query_image_display(self.capture)

    def start_capture(self):
        """
        Load the ScreenCapture instance and let user capture the screen. 
        Switches query mode to image query.
        
        """
        screencapturer = ScreenCapture()
        screencapturer.showFullScreen()
        screencapturer.exec()

        # Emit the capture to display
        self.capture = screencapturer.get_capture()
        self.searchbox_signal_instance.capture_done_signal.emit(self.capture)

        # Clear the file path searchbox and switch to image query mode
        self._use_image_query = True 
        self.clear_text_query() 

    @Slot()
    def on_screenshot_clicked(self):
        """
        Emit signal to close the main window, wait a bit, and call the screencapture method
        
        """
        # Emit signal to temporarily hide main window
        self.searchbox_signal_instance.capture_start_signal.emit()
        QTimer.singleShot(300, self.start_capture) # Delay the creation of screencapture overlay a bit to fully hide main window

    @Slot()
    def on_browse_clicked(self):
        """
        Allow user to browse the directory for a path to query, manually submit image to display since the textbox's 
        onchanged event uses textEdited (instead of textChanged) which
        doesn't automatically call the display pipeline
        
        :param self: Description
        """
        # Open a file dialog to select a file
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", filters)

        if file_path:
            self.searchbox.setText(file_path)
            self._use_image_query = False

            # Manually submit image to display
            tq = get_task_queue_instance()

            if os.path.isfile(file_path):
                tq.submit(lambda : utils.submit_query_display(file_path))
            else:
                tq.submit(utils.submit_query_clear)

    @Slot()
    def on_query_text_edited(self):
        """
        Display the query image based on whether the path currently in textbox is valid or not,
        if not, signal to clear the display. Any changes made to the textbox switches query mode to using
        path to query instead of image query through screenshot
        
        """
        path = self.searchbox.text()
        tq = get_task_queue_instance()
        self._use_image_query = False
    
        if os.path.isfile(path) and path.lower().endswith(SUPPORTED_IMAGE_FORMATS + ".pdf"):
            tq.submit(lambda : utils.submit_query_display(path))
        else:
            tq.submit(utils.submit_query_clear)

    def get_file_path(self):
        return self.searchbox.text()
    
    def get_capture(self):
        return self.capture
    
    def use_image_query(self):
        """
        Returns current query mode (Image query or Path query)
        
        """
        return self._use_image_query

class DatabaseSearchBoxWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Label
        self.label = QtWidgets.QLabel("From Database ")
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.adjustSize()

        # Create a drop down component
        client = get_client()
        database_paths = client.request_db_paths()
        self.folderbox = QtWidgets.QComboBox()
        self.folderbox.addItems(database_paths)

        # Layout setup
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        
        # Apply layout to database searchbox
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.folderbox)
        self.setLayout(self.layout)

    def get_selected_database(self):
        return self.folderbox.currentText()

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
        self.searchbar_layout = QtWidgets.QHBoxLayout()
        self.layout = QtWidgets.QVBoxLayout()

        # Apply layout to search components
        self.searchbar_layout.addWidget(self.file_searchbox)
        self.searchbar_layout.addWidget(self.search_button)
        self.layout.addLayout(self.searchbar_layout)
        self.layout.addWidget(self.database_searchbox)
        self.setLayout(self.layout)

    @Slot()
    def on_search_clicked(self):
        database_path = self.database_searchbox.get_selected_database()
        tq = get_task_queue_instance()

        if not self.file_searchbox.use_image_query(): # Use file path as query
            file_path = self.file_searchbox.get_file_path()

            if os.path.isfile(file_path) and os.path.isdir(database_path):
                future = tq.submit(lambda: utils.query(file_path, database_path))
                future.add_done_callback(utils.query_done)

        else: # Use image as query
            capture = self.file_searchbox.get_capture()
            if capture is not None and os.path.isdir(database_path):
                future = tq.submit(lambda: utils.query_using_image(capture, database_path))
                future.add_done_callback(utils.query_done)


        

        
