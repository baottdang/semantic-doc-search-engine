from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Qt
from services.threads.gallery_worker import get_gallery_worker_instance
from ui.main_area.gallery_controller.gallery_controller_utils import render_file
from ui.searchbox.searchbox_signal import get_searchbox_signal_instance
from ui.main_area.gallery_controller.gallery_controller_signal import get_gallery_controller_signal_instance
from ui.error.error_signal import get_error_signal_instance

class GalleryController():
    def __init__(self, viewport):
        # Gallery control
        self._index = 0
        self._files = [] # List of file results in format (path, page, score)
        self.viewport = viewport
        self._task_id = 0

        # Signal 
        self.searchbox_signal_instance = get_searchbox_signal_instance()
        self.searchbox_signal_instance.query_complete_signal.connect(self.load_controller)

    def load_controller(self, results):
        """
        Load the (path, page, score) list into the controller and submit the first result for display

        :param results: List of results, where result = (path, page, score)
        """
        self._files = results
        self._index = 0
        # Submit the first result to display
        if len(self._files) > 0:
            path, page, score = self._files[0]
            self.submit_pixmap(path, page, score)
        # Submit to clear the display
        else:
            self.submit_pixmap("", "", "") # Submit ("", "", "") to clear the display

    def submit_pixmap(self, path, page, score):
        """
        Load file as pixmap, submit signal to display
        
        :param path: Path to file
        :param page: Page of file
        :param score: Similarity score
        """
        worker = get_gallery_worker_instance()

        viewport_width = self.viewport.width()  
        viewport_height = self.viewport.height()  

        self._task_id += 1
        task_id = self._task_id

        # Submit to render metadata
        gallery_controller_signal_instance = get_gallery_controller_signal_instance()
        gallery_controller_signal_instance.changed_page_signal.emit(path)

        # Submit to render image
        future = worker.submit(lambda : render_file(path=path, page=page, viewport_height=viewport_height, viewport_width=viewport_width, task_id=task_id, dpi=80))
        future.add_done_callback(lambda future : self.done_get_qimage_callback(future, path, page, score))

    def done_get_qimage_callback(self, future, path, page, score):
        """
        Callback for when QImage of file is created, emit signal for display
        
        :param future: Future instance
        """
        try:
            qimage, task_id = future.result()

            # Drop stale tasks
            if task_id != self._task_id:
                return
            
            if qimage is None and path != "":
                print("No image") # Placeholder for could not retrieve file, replace with Error Icon later
            else:
                gallery_controller_signal_instance = get_gallery_controller_signal_instance()
                gallery_controller_signal_instance.done_get_pixmap_signal.emit(qimage, path, str(page), str(score))
        except Exception as e:
            import traceback
            print("Task raised exception:", e)
            traceback.print_exc()
            error_instance = get_error_signal_instance()
            error_instance.error_signal.emit("Error", f"Error while getting pixmap\nError message: {e}")
        
    @Slot()
    def next_file(self):
        if self._index <= len(self._files) - 2:
            self._index += 1

            path, page, score = self._files[self._index]
            self.submit_pixmap(path, page, score)

    @Slot()
    def previous_file(self):
        if self._index >= 1:
            self._index -= 1

            path, page, score = self._files[self._index]
            self.submit_pixmap(path, page, score)

class GalleryControllerWidget(QtWidgets.QWidget):
    def __init__(self, viewport, parent=None):
        super().__init__(parent)

        # Components
        self.controller = GalleryController(viewport)
        self.left_button = QtWidgets.QPushButton("<")
        self.right_button = QtWidgets.QPushButton(">")
        self.show_controller = False 
        self.setVisible(self.show_controller)

        self.left_button.clicked.connect(self.controller.previous_file)
        self.left_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.right_button.clicked.connect(self.controller.next_file)
        self.right_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # Signal 
        self.searchbox_signal_instance = get_searchbox_signal_instance()
        self.searchbox_signal_instance.query_complete_signal.connect(self.show_or_hide_controller)

        # Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.left_button)
        self.buttons_layout.addWidget(self.right_button)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    @Slot()
    def show_or_hide_controller(self, results):
        if len(results) <= 1:
            self.show_controller = False
        else:
            self.show_controller = True
        self.setVisible(self.show_controller)

