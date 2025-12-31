from PySide6.QtCore import QObject, Signal

class ConstructSignal(QObject):
    # Signals
    construct_complete_signal = Signal(str, str, name="index_construct_complete")
    construct_error_signal = Signal(str, name="construct_error_signal")

# Singleton instance
construct_signal = None

def get_construct_signal_instance():
    global construct_signal
    if not construct_signal:
        construct_signal = ConstructSignal()
    return construct_signal