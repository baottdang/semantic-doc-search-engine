from services.db_interface.db_manager import get_db_manager

class ListActionExecutor:
    def __init__(self):
        self.db_manager = get_db_manager()

    def delete_database(self, db_name):
        return self.db_manager.drop(db_name)
