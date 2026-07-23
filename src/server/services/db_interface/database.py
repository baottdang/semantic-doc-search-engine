from services.index.index_construct_utils import path_to_dbname
from services.db_interface.db_api import get_db_api_instance

class DatabaseTable():
    def __init__(self, name, folder_path, index_model, date_indexed=""):
        self.table_name = name
        self.folder_path = folder_path
        self.index_model = index_model
        self.date_indexed = date_indexed
        self.api = get_db_api_instance()
        self.api.create_table(self.table_name, folder_path, index_model)

    def insert(self, path, page_num, feature):
        self.api.insert_to_table(self.table_name, path, page_num, feature)

    def bulk_insert(self, package):
        self.api.bulk_insert(self.table_name, package)

    def create_hnsw_index(self, d_func, m, ef_construction):
        self.api.create_hnsw_index_in_table(self.table_name, d_func, m, ef_construction)

    def query_embedding(self, embedding, num_result):
        return self.api.query_embedding(self.table_name, embedding, num_result)

    def get_info(self):
        return self.table_name, self.folder_path, self.index_model, self.date_indexed

    def commit(self):
        self.api.commit()

    def close_connection(self):
        self.api.close_connection()