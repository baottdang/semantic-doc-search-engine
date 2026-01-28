from PySide6.QtCore import Signal, QObject

class SettingSignal(QObject):
    setting_saved_signal = Signal(name="setting_saved_signal")

# Singleton instance
setting_signal_instance = None

def get_setting_signal_instance():
    global setting_signal_instance
    if setting_signal_instance is None:
        setting_signal_instance = SettingSignal()
    return setting_signal_instance