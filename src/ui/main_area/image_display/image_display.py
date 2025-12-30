from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Qt
from ui.main_area.canvas.canvas_painter import CanvasPainter
from ui.main_area.gallery_controller.gallery_controller_signal import get_gallery_controller_signal_instance
from ui.main_area.query_image_controller.query_image_controller_signal import get_query_image_controller_signal_instance
from ui.error.error_signal import get_error_signal_instance
from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS
import os
import webbrowser

class ImageDisplay(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # Components
        self.path_label = QtWidgets.QLabel()
        self.path_label.setAlignment(Qt.AlignCenter)
        self.canvas = CanvasPainter()
        self.page_label = QtWidgets.QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.page_label)
        self.setLayout(self.layout)

    def set_path_text(self, path):
        self.path_label.setText(path)

    def set_page_text(self, page):
        self.page_label.setText(page)

    def set_image(self, qimage):
        self.canvas.update_image(qimage)

    def get_viewport(self):
        return self.canvas
    
    def update_scale_image(self):
        self.canvas.update_scale_image()

    @Slot()
    def display(self, qimage, path, page):
        self.set_image(qimage)
        self.set_path_text(path)
        if page != "":
            self.set_page_text(f"Page:{page}")
        else:
            self.set_page_text("")

class ImageResultDisplay(ImageDisplay):
    def __init__(self, parent):
        super().__init__(parent)

        # Context menu for file opening actions
        self.context_menu = QtWidgets.QMenu(self)
        open_file_action = self.context_menu.addAction("Open File")
        open_file_location_action = self.context_menu.addAction("Open File location")
 
        # Connect the actions to methods
        open_file_action.triggered.connect(self.open_file_triggered)
        open_file_location_action.triggered.connect(self.open_file_location_triggered)

        # Signal
        self.gallery_controller_signal_instance = get_gallery_controller_signal_instance()
        self.gallery_controller_signal_instance.done_get_pixmap_signal.connect(self.display)

    @Slot()
    def open_file_triggered(self):
        try:
            os.startfile(self.path_label.text())
        except Exception as e:
            error_instance = get_error_signal_instance()
            error_instance.error_signal.emit("File Error", f"Could not open file: {self.path_label.text()}")

    @Slot()
    def open_file_location_triggered(self):
        # Open the folder containing the file
        os.startfile(os.path.dirname(self.path_label.text()))

    def contextMenuEvent(self, event):
        if os.path.exists(self.path_label.text()):
            self.context_menu.exec(event.globalPos())
    
class ImageQueryDisplay(ImageDisplay):
    def __init__(self, parent):
        super().__init__(parent)
        # Signals
        self.query_image_controller_signal_instance = get_query_image_controller_signal_instance()
        self.query_image_controller_signal_instance.done_get_query_pixmap_signal.connect(self.display)
        self.query_image_controller_signal_instance.clear_query_signal.connect(self.clear)

    @Slot()
    def display(self, qimage, path, page):
        if qimage is not None:
            self.set_image(qimage)
            self.set_path_text(path)
            if page != "":
                self.set_page_text(f"Page:{page}")
            else:
                self.set_page_text("")

    @Slot()
    def clear(self):
        """
        Clear the canvas if an image is present
        
        :param self: Description
        """
        if not self.canvas.is_empty():
            self.set_image(None)
        self.set_path_text("")
        self.set_page_text("")
