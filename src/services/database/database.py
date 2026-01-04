import sqlite3
from resources.strings.string_resource import database_path

class Database:
    def __init__(self, path):
        self._database_path = path
        self._conn = sqlite3.connect(self._database_path)
        self._cursor = self._conn.cursor()
        self.load_database()

    def get_indexed_database_paths(self):
        self._cursor.execute("SELECT database_path FROM index_info")
        result = self._cursor.fetchall()
        return [row[0] for row in result]

    def get_database_names(self):
        self._cursor.execute("SELECT index_name FROM index_info")
        result = self._cursor.fetchall()
        return [row[0] for row in result]
    
    def load_database(self):
        """
        Load the SQLite database. If database does not exist, create a new one.
        """
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS index_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                index_name STRING UNIQUE NOT NULL,
                index_path STRING UNIQUE NOT NULL,
                database_path STRING UNIQUE NOT NULL
            )
            """
        )
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS index_entries (
                index_id INTEGER PRIMARY KEY,
                index_name TEXT NOT NULL,
                path TEXT NOT NULL,
                page INTEGER NOT NULL
            )
            """
        )
        self.commit()

    def get_next_index_id(self):
        """Get the next available index ID for a new entry."""
        self._cursor.execute("SELECT MAX(index_id) FROM index_entries")
        result = self._cursor.fetchone()
        max_id = result[0] if result[0] is not None else 0
        return max_id + 1
    
    def add_index_entry(self, index_id, index_name, path, page, commit=False):
        self._cursor.execute("INSERT OR REPLACE INTO index_entries (index_id, index_name, path, page) VALUES (?, ?, ?, ?)", (index_id, index_name, path, page))
        if commit:
            self.commit()

    def get_index_entry(self, id):
        self._cursor.execute("SELECT * FROM index_entries WHERE index_id = ?", (id,))
        return self._cursor.fetchone()

    def commit(self):
        self._conn.commit()

    def close_connection(self):
        self._conn.close()

    def add_database_info(self, name, database_path, index_path):
        self._cursor.execute("INSERT OR REPLACE INTO index_info (index_name, index_path, database_path) VALUES (?, ?, ?)", (name, index_path, database_path))
        self.commit()

    def get_indices(self):
        self._cursor.execute("SELECT * FROM index_info")
        return self._cursor.fetchall()

# Singleton instance of Database
_db = None

def get_main_database_instance():
    """
    Returns the database instance to be used in main thread.
    Implementation must init a separate Database object if used in workers.
    """
    global _db
    if _db is None:
        _db = Database(database_path)
    return _db