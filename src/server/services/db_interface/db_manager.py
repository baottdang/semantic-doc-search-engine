from services.db_interface.db_api import get_db_api_instance
from services.db_interface.db_manager_signal import get_db_manager_signal_instance
from services.db_interface.database import DatabaseTable

class DatabaseManager():
    def __init__(self):
        self.tables = {}
        self.init_tables()
        self.db_manager_signal = get_db_manager_signal_instance()

    def init_tables(self):
        db_api = get_db_api_instance()
        table_infos = db_api.get_table_infos() # Returns lists of table infos (id, ref, tablename, path, date_indexed, index used)
        for tb_info in table_infos:
            _, tb_name, tb_path, index_model, date_indexed = tb_info
            table = DatabaseTable(tb_name, tb_path, index_model, date_indexed)
            self.tables[tb_name] = table

    def insert_table(self, name, table):
        self.tables[name] = table

    def get_table(self, name):
        if name in self.tables:
            return self.tables[name]
        return ""
    
    def drop(self, name):
        if name in self.tables:
            table = self.tables[name]
            db_api = get_db_api_instance()
            if db_api.drop_table(table.table_name):
                del self.tables[name]
                self.db_manager_signal.drop_sucess_signal.emit(table.folder_path)
                return True
            else:
                self.db_manager_signal.drop_error_signal.emit(table.folder_path)
                return False
            
    def is_indexed(self, path):
        db_api = get_db_api_instance()
        return db_api.is_indexed(path)
    
    def get_db_paths(self):
        db_api = get_db_api_instance()
        return db_api.get_db_paths()
    
    def close_tables(self, name):
        self.tables[name].close_connection()

_db_manager = DatabaseManager()

def get_db_manager():
    return _db_manager