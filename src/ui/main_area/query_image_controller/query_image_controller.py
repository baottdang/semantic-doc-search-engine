from ui.searchbox.searchbox_signal import get_searchbox_signal_instance
from services.threads.taskqueue import get_task_queue_instance
from ui.main_area.gallery_controller.gallery_controller_utils import render_file
from ui.error.error_signal import get_error_signal_instance
from ui.main_area.query_image_controller.query_image_controller_signal import get_query_image_controller_signal_instance
import os

class QueryImageController():
    def __init__(self, viewport):
        # Query controller components
        self._path = ""
        self._image = None
        self._task_id = 0
        self.viewport = viewport
        
        # Signals
        self.searchbox_signal_instance = get_searchbox_signal_instance()
        self.searchbox_signal_instance.query_changed_signal.connect(self.load_controller)
        self.searchbox_signal_instance.query_cleared_signal.connect(self.clear_query)
        self.searchbox_signal_instance.query_image_done_signal.connect(self.load_image)
    
    def load_controller(self, path):
        self._path = path
        if path != "":
            self.submit_pixmap(path, 1)

    def load_image(self, qimage):
        self._image = qimage
        if qimage is not None:
            self.submit_image(qimage)

    def clear_query(self):
        query_image_controller_signal_instance = get_query_image_controller_signal_instance()
        query_image_controller_signal_instance.clear_query_signal.emit()
        print("Clearing")

    def submit_image(self, qimage):
        query_image_controller_signal_instance = get_query_image_controller_signal_instance()
        query_image_controller_signal_instance.done_get_query_pixmap_signal.emit(qimage, "QLEN-SCREENSHOT", str(1))

    def submit_pixmap(self, path, page):
        """
        Load file as pixmap, submit signal to display
        
        :param path: Path to file
        :param page: Page of file
        :param score: Similarity score
        """
        worker = get_task_queue_instance()

        viewport_width = self.viewport.width()  
        viewport_height = self.viewport.height()  

        self._task_id += 1
        task_id = self._task_id

        future = worker.submit(lambda : render_file(path=path, page=page, viewport_height=viewport_height, viewport_width=viewport_width, task_id=task_id, dpi=80))
        future.add_done_callback(lambda future : self.done_get_qimage_callback(future, path, page))

    def done_get_qimage_callback(self, future, path, page):
        """
        Callback for when QImage of file is created, emit signal for display
        
        :param future: Future instance
        """
        try:
            qimage, task_id = future.result()

            # Drop stale tasks
            if task_id != self._task_id:
                return
            
            if qimage is None and os.path.isfile(path):
                print("No image") # Placeholder for could not retrieve file, replace with Error Icon later
            else:
                query_image_controller_signal_instance = get_query_image_controller_signal_instance()
                query_image_controller_signal_instance.done_get_query_pixmap_signal.emit(qimage, path, str(page))
        except Exception as e:
            import traceback
            print("Task raised exception:", e)
            traceback.print_exc()
            error_instance = get_error_signal_instance()
            error_instance.error_signal.emit("Error", f"Error while getting pixmap\nError message: {e}")
