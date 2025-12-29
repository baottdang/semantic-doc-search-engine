from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage

class ScreenCaptureSignal(QObject):
    capture_done_signal = Signal(QImage, name="capture_done_signal")

# Singleton instance
screencapture_signal_instance = None

def get_screencapture_signal_instance():
    global screencapture_signal_instance
    if screencapture_signal_instance is None:
        screencapture_signal_instance = ScreenCaptureSignal()
    return screencapture_signal_instance