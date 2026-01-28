from resources.strings.string_resource import database_path
from services.database.database import Database
from services.filewatcherservice.action_journal import ActionJournal
from services.index.index_construct import add_files_to_indices
import time, threading

class IndexerService:
    def __init__(self):
        self.journal = ActionJournal()
        self.database = Database(database_path)

    def process_actions(self, actions):
        """
        Process in the actions
        
        :param actions: List of tuples containing action infos
        """
        from services.indexer.indexersignal import get_indexer_signal_instance
        new_files = []
        ids = []
        for action in actions:
            id, op_code, old_path, new_path, index_name = action
            if op_code == 0: # File added
                new_files.append((new_path, index_name))
            elif op_code == 1: # File deleted
                self.database.remove_file(old_path)
            elif op_code == 2: # File moved (or renamed)
                self.database.update_file(old_path, new_path)
            ids.append(id)

        # Process new files
        add_files_to_indices(new_files)

        # Signal new files completion
        indexer_signal_instance = get_indexer_signal_instance()
        indexer_signal_instance.added_files_signal.emit(len(new_files))

        # Mark files as processed
        self.journal.mark_processed(ids)

    def run(self):
        while(True):
            actions = self.journal.get_unprocessed_actions()
            if len(actions) == 0:
                time.sleep(2)
            else:
                self.process_actions(actions)

def start_indexer():
    indexer = IndexerService()
    indexer.run() # Blocking

def load_indexer_thread():
    t = threading.Thread(target=start_indexer, daemon=True, name="IndexerServiceThread")
    t.start()
