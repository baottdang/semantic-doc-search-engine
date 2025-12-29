from PySide6.QtCore import Signal, QObject

class IndexSignal(QObject):
    # Signals
    index_start_signal = Signal(str, name="index_start")
    index_complete_signal = Signal(str, str, name="index_complete")

# Singleton instance
index_signal = None

def get_index_signal_instance():
    global index_signal
    if not index_signal:
        index_signal = IndexSignal()
    return index_signal