from PySide6.QtCore import Signal, QObject

class IndexerSignal(QObject):
    added_files_signal = Signal(int, name="added_files_signal")

# Singleton instance
indexer_signal_instance = None

def get_indexer_signal_instance():
    global indexer_signal_instance
    if indexer_signal_instance is None:
        indexer_signal_instance = IndexerSignal()
    return indexer_signal_instance