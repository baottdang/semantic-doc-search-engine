from ui.setting.setting_signal import get_setting_signal_instance
from resources.strings.string_resource import config_path, wdname, wdpath
from services.threads.taskqueue import get_task_queue_instance
from ui.error.error_signal import get_error_signal_instance
import configparser, winreg

class SettingManager:
    def __init__(self):
        self.setting_signal_instance = get_setting_signal_instance()
        self.setting_signal_instance.setting_saved_signal.connect(self.execute_changes)
        self.error_instance = get_error_signal_instance()

    def execute_changes(self):
        tq = get_task_queue_instance()
        tq.submit(self.execute_changes_helper)

    def execute_changes_helper(self):
        config = configparser.ConfigParser()
        config.read(config_path)
        if "filewatcher" in config:
            if config.getboolean("filewatcher", "enabled"):
                self.add_wd_to_startup()
            else:
                self.remove_wd_from_startup()

    def add_wd_to_startup(self):
        error_occured = False
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            ) as key:
                try:
                    current_value, _ = winreg.QueryValueEx(key, wdname) 
                    if current_value == wdpath:
                        return
                    else:
                        winreg.SetValueEx(key, wdname, 0, winreg.REG_SZ, wdpath)
                except FileNotFoundError:
                    winreg.SetValueEx(key, wdname, 0, winreg.REG_SZ, wdpath)
        except FileNotFoundError:
            self.error_instance.error_signal.emit("Registry Error", "Registry path not found.")
            error_occured = True
        except PermissionError:
            self.error_instance.error_signal.emit("Registry Error", "Permission denied. Try running as administrator.")
            error_occured = True
        except OSError as e:
            self.error_instance.error_signal.emit("Registry Error", f"Unexpected error: {e}")
            error_occured = True
        finally:
            if error_occured:
                config = configparser.ConfigParser()
                config.read(config_path)
                if "filewatcher" in config:
                    config["filewatcher"]["enabled"] = "False"
                    with open(config_path, "w") as f:
                        config.write(f)

    def remove_wd_from_startup(self):
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        error_occured = False
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                reg_path,
                0,
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.DeleteValue(key, wdname)
        except FileNotFoundError:
            self.error_instance.error_signal.emit("Registry Error", f"No startup entry named '{wdname}' found.")
            error_occured = True
        except PermissionError:
            self.error_instance.error_signal.emit("Registry Error", "Permission denied. Try running as administrator.")
            error_occured = True
        except OSError as e:
            self.error_instance.error_signal.emit("Registry Error", f"Unexpected error: {e}")
            error_occured = True
        finally:
            if error_occured:
                config = configparser.ConfigParser()
                config.read(config_path)
                if "filewatcher" in config:
                    config["filewatcher"]["enabled"] = "True"
                    with open(config_path, "w") as f:
                        config.write(f)


        