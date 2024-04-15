import sqlite3
from contextlib import contextmanager

database = './hw.db'


@contextmanager
def create_connection(db_file):
    """ Create a database connection to SQLite database """

    conn = sqlite3.connect(db_file)
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()

