from services.database.database import get_main_database_instance
from ui.error.error_signal import get_error_signal_instance
from resources.strings.string_resource import database_path
from services.database.database import Database
import os

class Index():
    def __init__(self, parent=None):
        self.indices = {}
        self.load_indices()

    def load_indices(self):
        """
        Load indices from database to a map of name : path
        
        """
        import faiss
        
        database = get_main_database_instance()
        index_list = database.get_indices()
        for _, _, index_path, database_path in index_list:
            if os.path.isfile(index_path):
                self.indices[database_path] = faiss.read_index(index_path)
            else: # Replace this later with more robust error handling
                error_instance = get_error_signal_instance()
                error_instance.error_signal.emit("Index Error", f"Could not find index of {database_path}")
                continue

    def get_index(self, database_path):
        """
        Return the index using its path
        
        :param path: path of index
        """
        try:
            return self.indices[database_path]
        except KeyError as e:
            return None
    
    def add_new_index_to_mem(self, index, database_path):
        self.indices[database_path] = index

    def remove_index(self, indexed_database_path):
        """
        Remove the index from the list and the disk
        Index still lives in memory to avoid query issues
        
        :param database_path: Path to database
        """
        db = Database(database_path)
        self.indices.pop(indexed_database_path, None)

        index_info = db.get_index_info(database_path=indexed_database_path)
        index_path = index_info[2]

        if os.path.exists(index_path): 
            os.remove(index_path)
            
    
# Singleton instance
index = None

def get_index_instance():
    global index
    if index is None:
        index = Index()
    return index