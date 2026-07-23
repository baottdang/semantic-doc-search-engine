from PySide6.QtCore import QObject, Signal
from numpy import ndarray

class QueryImageControllerSignal(QObject):
    # Signals
    done_get_query_pixmap_signal = Signal(ndarray, str, str, name="done_get_query_pixmap_signal")
    clear_query_signal = Signal(name="clear_query_signal")

# Singleton instance
gallery_controller_signal_instance = None

def get_query_image_controller_signal_instance():
    global gallery_controller_signal_instance

    if gallery_controller_signal_instance is None:
        gallery_controller_signal_instance = QueryImageControllerSignal()
        
    return gallery_controller_signal_instance