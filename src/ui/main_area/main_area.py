from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from ui.main_area.image_display.image_display import ImageResultDisplay, ImageQueryDisplay
from ui.main_area.gallery_controller.gallery_controller import GalleryControllerWidget
from ui.main_area.query_image_controller.query_image_controller import QueryImageController

class MainArea(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Components
        self.query_display = ImageQueryDisplay(self)
        self.result_display = ImageResultDisplay(self)
        self.toggle_show_query_button = QtWidgets.QPushButton("Hide Query")
        self.toggle_show_query_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.toggle_show_query_button.clicked.connect(self.toggle_show_query)
        self.gallery_controller_widget = GalleryControllerWidget(self.result_display.get_viewport())
        self.query_image_controller = QueryImageController(self.query_display.get_viewport())
        self._show_query = True
        
        # Layout
        self.display_layout = QtWidgets.QHBoxLayout()
        self.display_layout.addWidget(self.query_display)
        self.display_layout.addWidget(self.result_display)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.toggle_show_query_button)
        self.main_layout.addLayout(self.display_layout)
        self.main_layout.addWidget(self.gallery_controller_widget)
        self.setLayout(self.main_layout)

    @Slot()
    def toggle_show_query(self):
        self._show_query = not self._show_query
        self.query_display.setVisible(self._show_query)
        if self._show_query == True:
            self.toggle_show_query_button.setText("Hide Query")
        else:
            self.toggle_show_query_button.setText("Show Query")
        self.result_display.update_scale_image()

    def show_result(self, path, page, pixmap):
        self.result_display.set_page_text(path)
        self.result_display.set_page_text(page)
        self.result_display.set_image_pixmap(pixmap)

    def clear_result(self):
        self.result_display.set_page_text("")
        self.result_display.set_page_text("")
        self.result_display.set_image_pixmap(None)

    def show_query(self, path, page, pixmap):
        self.query_display.set_page_text(path)
        self.query_display.set_page_text(page)
        self.query_display.set_image_pixmap(pixmap)

    def clear_query(self):
        self.query_display.set_page_text("")
        self.query_display.set_page_text("")
        self.query_display.set_image_pixmap(None)

    def resizeEvent(self, event):
        self.result_display.update_scale_image()
        self.query_display.update_scale_image()


