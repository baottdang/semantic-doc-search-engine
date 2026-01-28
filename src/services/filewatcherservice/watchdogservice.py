import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from services.filewatcherservice.action_journal import ActionJournal
from resources.strings.string_resource import ALL_SUPPORTED_FORMAT, icon_path
from services.database.database import get_main_database_instance
from services.filewatcherservice.action_queue import get_action_queue_instance
from PIL import Image

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, fpath):
        super().__init__()
        self.journal = ActionJournal()
        self.actionqueue = get_action_queue_instance()
        self.fpath = fpath

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(ALL_SUPPORTED_FORMAT):
            self.actionqueue.submit(self.journal.add_change, 0, "", event.src_path, self.fpath)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.lower().endswith(ALL_SUPPORTED_FORMAT):
            self.actionqueue.submit(self.journal.add_change, 1, event.src_path, "", "")

    def on_moved(self, event):
        if not event.is_directory and event.src_path.lower().endswith(ALL_SUPPORTED_FORMAT):
            self.actionqueue.submit(self.journal.add_change, 2, event.src_path, event.dest_path, "")

class WatchDog:
    def __init__(self, folder_paths):
        self.observer = None
        self.fpaths = folder_paths

    def start(self):
        self.observer = Observer()

        for fpath in self.fpaths:
            if os.path.exists(fpath):
                 event_handler = FileEventHandler(fpath)
                 self.observer.schedule(event_handler, path=fpath, recursive=True)

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def run_tray(self):
        import pystray

        icon = pystray.Icon(
            "Qlen Watchdog Service",
            icon=Image.open(icon_path) # Placeholder
        )
        icon.run() 

if __name__ == "__main__":
    db = get_main_database_instance()
    wd = WatchDog(db.get_indexed_database_paths())
    wd.run_tray()