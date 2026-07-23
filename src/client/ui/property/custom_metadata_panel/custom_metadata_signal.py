from PySide6.QtCore import QObject, Signal

class CustomMetadataSignal(QObject):
    done_get_xmp_metadata_signal = Signal(dict, name="done_get_xmp_metadata_signal")

# Singleton instance
custom_metadata_signal_instance = None

def get_custom_metadata_signal_instance():
    global custom_metadata_signal_instance
    if custom_metadata_signal_instance is None:
        custom_metadata_signal_instance = CustomMetadataSignal()
    return custom_metadata_signal_instance