import sqlite3
from resources.strings.string_resource import journal_path

class ActionJournal:
    def __init__(self):
        self._path = journal_path
        self.load_journal()

    def load_journal(self):
        """
        Load the SQLite database. If database does not exist, create a new one.

        Opcode: 0 - ADD, 1 - DELETE, 2 - MOVE
        """
        conn = sqlite3.connect(self._path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                op_code INTEGER,
                old_path TEXT,
                new_path TEXT,
                index_name TEXT,
                processed INTEGER
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS action_unprocessed
            ON action_journal(id)
            WHERE processed = 0;
            """
        )
        conn.commit()
        conn.close()

    def add_change(self, op_code, old_path="", new_path="", index_name=""):
        """
        Record file changes to journal, leave old_path blank when ADD, leave new_path blank when DELETE. 

        Opcode: 0 - ADD, 1 - DELETE, 2 - MOVE
        """
        conn = sqlite3.connect(self._path)
        cursor = conn.cursor()

        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")

        cursor.execute("INSERT INTO action_journal (op_code, old_path, new_path, index_name, processed) VALUES (?, ?, ?, ?, ?)", (op_code, old_path, new_path, index_name, 0))
        try:
            conn.commit()
            conn.close()
        except Exception as e:
            pass

    def get_unprocessed_actions(self):
        conn = sqlite3.connect(journal_path)
        cur = conn.cursor()

        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")

        conn.execute(
            """
            SELECT id, op_code, old_path, new_path, index_name
            FROM action_journal
            WHERE processed = 0
            ORDER BY id
            LIMIT 50;
            """
        )
        actions = cur.fetchall()
        return actions
    
    def mark_processed(self, ids):
        conn = sqlite3.connect(journal_path)

        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")

        placeholders = ",".join("?" for _ in ids)

        conn.execute(f"UPDATE FROM action_journal SET processed = 1 WHERE id IN ({placeholders})", ids)

        try:
            conn.commit()
            conn.close()
        except Exception as e:
            pass

