from PySide6.QtCore import QObject, Signal

class DefaultMetadataPanelSignal(QObject):
    # Signal
    metadata_returned_signal = Signal(dict, name="metadata_returned_signal")

# Singleton instance
signal_instance = None

def get_default_metadata_signal_instance():
    global signal_instance
    if signal_instance is None:
        signal_instance = DefaultMetadataPanelSignal()
    return signal_instance