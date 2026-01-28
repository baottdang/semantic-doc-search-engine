from PySide6 import QtWidgets
from resources.strings.string_resource import config_path
from ui.setting.setting_signal import get_setting_signal_instance
from ui.setting.setting_manager import SettingManager
import configparser

class SettingWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setFixedWidth(400)
        self.setFixedHeight(150)

        self.setting_signal_instance = get_setting_signal_instance()
        self.manager = SettingManager()

        # Config Component
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        if "filewatcher" not in self.config:
            self.config["filewatcher"] = {"enabled" : False}

        # UI components
        self.boot_watchdog_with_windows = QtWidgets.QCheckBox("Boot File Watcher service alongside Windows")
        self.boot_watchdog_with_windows.setChecked(self.config.getboolean("filewatcher", "enabled"))

        self.save_settings_button = QtWidgets.QPushButton("Save Settings")
        self.save_settings_button.clicked.connect(self.save_setting_to_cfg)
        
        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.boot_watchdog_with_windows)
        self.layout.addWidget(self.save_settings_button)

        self.setLayout(self.layout)

    def save_setting_to_cfg(self):
        if str(self.boot_watchdog_with_windows.isChecked()) != self.config["filewatcher"]["enabled"]: # Save only when the values in config file and current are different
            self.config["filewatcher"]["enabled"] = str(self.boot_watchdog_with_windows.isChecked())

            with open(config_path, "w") as f:
                self.config.write(f)

            self.setting_signal_instance.setting_saved_signal.emit()



