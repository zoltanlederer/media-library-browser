""" All database queries live here """

import sqlite3

def get_connection(db_path='data/media.db'):
    """Opens and returns a connection to the database"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # rows behave like dictionaries — access by column name instead of index
    return conn


def create_collections_table(conn):
    """Creates the collections table in the database if it doesn't already exist"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        imdb_id TEXT NOT NULL)
    ''')
    conn.commit()



    