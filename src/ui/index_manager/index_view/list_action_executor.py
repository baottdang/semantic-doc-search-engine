from ui.index_manager.index_view.listview_signal import get_listview_signal_instance
from services.database.database import Database
from services.threads.taskqueue import get_task_queue_instance
from resources.strings.string_resource import database_path
from services.index.index import get_index_instance
from services.threadlock.threadlock import get_index_rw_lock_instance
from PySide6.QtCore import Slot

class ListActionExecutor:
    def __init__(self):
        self.tq = get_task_queue_instance()
        self.index_manager = get_index_instance()
        self.lock_instance = get_index_rw_lock_instance()

        # Signal
        self.signal_instance = get_listview_signal_instance()
        self.signal_instance.database_delete_signal.connect(self.delete_database)

    @Slot()
    def delete_database(self, indexed_db_path):
        self.tq.submit(lambda: self.delete_database_worker(indexed_db_path))
        
    def delete_database_worker(self, indexed_db_path):
        # Delete the database in map
        db = Database(database_path) # Worker's connection to the database
        db.delete_indexed_database(indexed_db_path)

        # Delete the index
        self.index_manager.remove_index_list(indexed_db_path)
