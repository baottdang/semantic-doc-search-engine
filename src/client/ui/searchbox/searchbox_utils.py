from services.query.query import query_path, query_image
from ui.error.error_signal import get_error_signal_instance
from ui.searchbox.searchbox_signal import get_searchbox_signal_instance
from PySide6.QtGui import QImage
import cv2
import numpy as np

def query(file_path, database_path):
    """
    Offloader function to worker thread
    
    :param file_path: Path to query
    :param database_path: Path to database
    """
    if file_path and database_path:
        results = query_path(file_path, database_path)

    return results

def query_using_image(image, database_path):
    """
    Offloader function to worker thread
    
    :param qimage: Query image
    :param database_path: Path to database
    """
    if image is not None and database_path:
        results = query_image(image, database_path)

    return results

def query_done(future):
    """
    Callback for when query completes. Run by worker
    
    :param future: Future instance returned from submitting to task queue
    """
    try:
        results = future.result()
        for path, page, score in results:
            print(f"{path} in page {page} with similarity score: {score}")
        searchbox_signal_instance = get_searchbox_signal_instance()
        searchbox_signal_instance.query_complete_signal.emit(results)
    except Exception as e:
        import traceback
        print("Task raised exception:", e)
        traceback.print_exc()
        error_instance = get_error_signal_instance()
        error_instance.error_signal.emit("Error", f"Error while searching\nError message: {e}")

def submit_query_display(path):
    """
    Submit signal to display query image
    
    :param path: Description
    """
    if path != "":
        signal_instance = get_searchbox_signal_instance()
        signal_instance.query_changed_signal.emit(path)

def submit_query_image_display(image):
    """
    Submit signal to display query image
    
    :param qimage: Image of query
    """
    if image is not None:
        height, width, channels = image.shape
        bytes_per_line = channels * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).copy()
        
        signal_instance = get_searchbox_signal_instance()
        signal_instance.query_image_done_signal.emit(qimage)

def submit_query_clear():
    """
    Submit signal to clear query image
    
    :param path: Description
    """
    signal_instance = get_searchbox_signal_instance()
    signal_instance.query_cleared_signal.emit()
