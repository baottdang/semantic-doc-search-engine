from services.database.database import get_main_database_instance

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
            self.indices[database_path] = faiss.read_index(index_path)

    def get_index(self, path):
        """
        Return the index using its path
        
        :param path: path of index
        """
        return self.indices[path]
    
    def add_new_index_to_mem(self, index, database_path):
        self.indices[database_path] = index
    
# Singleton instance
index = None

def get_index_instance():
    global index
    if index is None:
        index = Index()
    return index