from PySide6.QtCore import QObject, Signal

class ListviewSignal(QObject):
    # Signal
    database_delete_signal = Signal(str, name="database_delete_signal")
    database_delete_complete_signal = Signal(str, name="database_delete_complete_signal")

# Singleton instance
signal_instance = None

def get_listview_signal_instance():
    global signal_instance
    if signal_instance is None:
        signal_instance = ListviewSignal()
    return signal_instance