from pgvector.psycopg import register_vector
from pgvector import Vector
from resources.strings.string_resource import d_model, host, postgresql_port, dbname, user, password, version
from psycopg import sql
import psycopg

class Api():
    def __init__(self, host, port, dbname, user, password):
        self.conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )

        register_vector(self.conn) # Registers vector datatype

        self.create_meta_table()

    def query_embedding(self, table, embedding, num_result):
        cur = self.conn.cursor()
        query = sql.SQL("""
            SELECT 
                filepath,
                page,
                embedding,
                embedding <-> %s AS distance
            FROM {table}
            ORDER BY embedding <-> %s
            LIMIT %s
        """).format(
            table=sql.Identifier(table)   # safely interpolate table name
        )

        cur.execute(query, (embedding, embedding, num_result))
        results = cur.fetchall()
        return results

    def create_meta_table(self):
        """
        Create a table for storing metadata
        """
        cur = self.conn.cursor()
        cur.execute(
                    sql.SQL("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id SERIAL PRIMARY KEY,
                    tablename TEXT UNIQUE,
                    path_on_disk TEXT,
                    index_model TEXT,
                    date_indexed TEXT
                )
            """)
        )

        self.conn.commit()

    def create_table(self, name, path, index_model):
        """
        Create a table for storing embeddings
        
        :param name: Name of table
        :param path: Path to the database folder on disk
        """
        cur = self.conn.cursor()
        cur.execute(
                    sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    filepath TEXT,
                    page INTEGER,
                    embedding VECTOR({})
                )
            """).format(
                sql.Identifier(name),
                sql.Literal(d_model)
            )
        )

        cur.execute(
            """
            INSERT INTO metadata (tablename, path_on_disk, index_model, date_indexed)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (tablename) DO NOTHING;
            """,
            (name, path, index_model, "1/2/3")
        )

        self.conn.commit()

    def get_table_infos(self):
        cur = self.conn.cursor()

        cur.execute("""
            SELECT * FROM metadata
        """)

        return cur.fetchall()
    
    def drop_table(self, table_name):
        cur = self.conn.cursor()

        try:
            cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(
                    sql.Identifier(table_name)
                )
            )

            cur.execute(
                """
                DELETE FROM metadata
                WHERE tablename = %s
                """,
                (table_name,)
            )

            self.conn.commit()
            return True

        except Exception as e:
            print("Error:", e)
            self.conn.rollback()
            return False

    def insert_to_table(self, table_name, file_path, page_num, embedding):
        cur = self.conn.cursor()
        cur.execute(
            sql.SQL("""
                INSERT INTO {} (filepath, page, embedding)
                VALUES (%s, %s, %s)
            """).format(
                sql.Identifier(table_name)
            ),
            (file_path, page_num, Vector(embedding))
        )

    def bulk_insert(self, table_name, package):
        cursor = self.conn.cursor()
        query = sql.SQL(
            "COPY {} (filepath, page, embedding) FROM STDIN"
        ).format(
            sql.Identifier(table_name)
        )

        with cursor.copy(query) as copy:
            for row in package:
                copy.write_row(row)

    def create_hnsw_index_in_table(self, table_name, d_func, m, ef_construction):
        cur = self.conn.cursor()
        cur.execute(
            sql.SQL("""
                CREATE INDEX ON {}
                USING hnsw (embedding {})
                WITH (
                    m = {},
                    ef_construction = {}
                );
            """).format(
                sql.Identifier(table_name),
                sql.SQL(d_func),
                sql.Literal(m),
                sql.Literal(ef_construction),
            )
        )

    def is_indexed(self, path):
        cur = self.conn.cursor()

        cur.execute(
            "SELECT EXISTS (SELECT 1 FROM metadata WHERE path_on_disk = %s)",
            (path,)
        )

        return cur.fetchone()[0]
    
    def get_db_paths(self):
        cur = self.conn.cursor()

        cur.execute(
            "SELECT (path_on_disk) FROM metadata"
        )
        results = cur.fetchall()
        return [path[0] for path in results]

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

_api = None

def get_db_api_instance():
    global _api
    if _api is None:
        _api = Api(host, postgresql_port, dbname, user, password)
    return _api