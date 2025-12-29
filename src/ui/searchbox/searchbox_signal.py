from PySide6.QtCore import Signal, QObject

class SearchBoxSignal(QObject):
    # Signals
    query_complete_signal = Signal(list, name="query_complete_signal")
    query_changed_signal = Signal(str, name="query_changed_signal")
    query_cleared_signal = Signal(name="query_changed_signal")

# Singleton instance
searchbox_signal_instance = None

def get_searchbox_signal_instance():
    global searchbox_signal_instance
    if searchbox_signal_instance is None:
        searchbox_signal_instance = SearchBoxSignal()
    return searchbox_signal_instance