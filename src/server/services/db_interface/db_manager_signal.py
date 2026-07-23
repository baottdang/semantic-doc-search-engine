from PySide6.QtCore import QObject, Signal

class DatabaseManagerSignal(QObject):
    # Signals
    drop_error_signal = Signal(str)
    drop_sucess_signal = Signal(str)

# Singleton instance
_db_manager_signal = None

def get_db_manager_signal_instance():
    global _db_manager_signal
    if not _db_manager_signal:
        _db_manager_signal = DatabaseManagerSignal()
    return _db_manager_signal