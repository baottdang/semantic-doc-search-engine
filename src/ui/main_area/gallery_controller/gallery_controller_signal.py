from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage

class GalleryControllerSignal(QObject):
    # Signals
    done_get_pixmap_signal = Signal(QImage, str, str, str, name="done_get_pixmap_signal")
    changed_page_signal = Signal(str, name="changed_page_signal")

# Singleton instance
gallery_controller_signal_instance = None

def get_gallery_controller_signal_instance():
    global gallery_controller_signal_instance
    if gallery_controller_signal_instance is None:
        gallery_controller_signal_instance = GalleryControllerSignal()
    return gallery_controller_signal_instance