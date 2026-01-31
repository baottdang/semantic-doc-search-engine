import time, os, threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from services.filewatcherservice.action_journal import ActionJournal
from ui.index_manager.index_view.listview_signal import get_listview_signal_instance
from resources.strings.string_resource import ALL_SUPPORTED_FORMAT, icon_path
from services.database.database import get_main_database_instance
from services.filewatcherservice.action_queue import get_action_queue_instance
from services.index.index_construct_signal import get_construct_signal_instance
from PySide6.QtCore import Slot
from PIL import Image

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, fpath):
        super().__init__()
        self.journal = ActionJournal()
        self.actionqueue = get_action_queue_instance()
        self.fpath = fpath

    def wait_for_file_ready(self, path, timeout=3.0, interval=0.1, stable_checks=3):
        start_time = time.time()
        last_size = None
        stable_count = 0

        while time.time() - start_time < timeout:
            try:
                size = os.path.getsize(path)

                if size == last_size:
                    stable_count += 1
                else:
                    stable_count = 0
                    last_size = size

                if stable_count >= stable_checks:
                    try:
                        with open(path, 'rb') as f:
                            f.read(1)
                        return True
                    except (OSError, PermissionError):
                        stable_count = 0  # reset and retry

            except FileNotFoundError:
                return False
            except OSError:
                pass

            time.sleep(interval)

        return False

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(ALL_SUPPORTED_FORMAT):
            if self.wait_for_file_ready(path=event.src_path):
                self.actionqueue.submit(self.journal.add_change, 0, "", event.src_path, self.fpath)
                print("added")

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.lower().endswith(ALL_SUPPORTED_FORMAT):
            self.actionqueue.submit(self.journal.add_change, 1, event.src_path, "", "")

    def on_moved(self, event):
        if not event.is_directory and event.src_path.lower().endswith(ALL_SUPPORTED_FORMAT):
            self.actionqueue.submit(self.journal.add_change, 2, event.src_path, event.dest_path, "")

class WatchDog:
    def __init__(self):
        self.observer = None
        self.db = get_main_database_instance()
        self.fpaths = self.db.get_indexed_database_paths()

        # Signals
        self.update_signal_instance = get_construct_signal_instance()
        self.update_signal_instance.construct_complete_signal.connect(self.update_watch_list)

        self.listview_signal_instance = get_listview_signal_instance()
        self.listview_signal_instance.database_delete_signal.connect(self.remove_from_watch)

        # Map of handlers and fpaths 
        self.event_handlers = {} 

    def start(self):
        self.observer = Observer()

        for fpath in self.fpaths:
            if os.path.exists(fpath):
                 event_handler = FileEventHandler(fpath)
                 self.event_handlers[fpath] = event_handler
                 self.observer.schedule(event_handler, path=fpath, recursive=True)

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    @Slot()
    def update_watch_list(self, index_path):
        self.fpaths.append(index_path) # Mismatch can happen here if index_path is not in database
        event_handler = FileEventHandler(index_path)
        self.observer.schedule(event_handler, path=index_path, recursive=True)

    @Slot()
    def remove_from_watch(self, database_path):
        self.observer.unschedule(self.event_handlers[database_path])

    def run_tray(self):
        import pystray

        icon = pystray.Icon(
            "Qlen Watchdog Service",
            icon=Image.open(icon_path) # Placeholder
        )
        icon.run() 

    def load_tray_thread(self):
        t = threading.Thread(target=self.run_tray, daemon=True, name="WatchdogTrayThread")
        t.start()

if __name__ == "__main__":
    wd = WatchDog()
    wd.load_tray_thread()
    wd.start()