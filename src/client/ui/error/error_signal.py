from PySide6.QtCore import Signal, QObject

class ErrorSignal(QObject):
    # Signals
    error_signal = Signal(str, str, name="error_signal")

# Singleton instance
error_instance = None

def get_error_signal_instance():
    global error_instance
    if error_instance is None:
        error_instance = ErrorSignal()
    return error_instance