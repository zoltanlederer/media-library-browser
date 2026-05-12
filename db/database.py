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


def get_all_media(filters):
    """Returns all titles matching the given filters"""
    # these two lists will build the WHERE clause dynamically
    conditions = []  # each filter becomes one condition e.g. 'type = ?'
    values = []      # the actual values that replace the ? placeholders

    # only add a condition if the filter was actually provided
    if filters.get('media_type'):
        conditions.append('type = ?')
        values.append(filters['media_type'])

    if filters.get('genres'):
        # genres is a comma-separated string e.g. "Comedy, Romance"
        # LIKE with % wildcards checks if the value appears anywhere in the string
        conditions.append('genres LIKE ?')
        values.append(f'%{filters["genres"]}%')

    if filters.get('cast'):
        # cast is also a comma-separated string — same LIKE approach
        # "cast" is in double quotes because it is a reserved word in SQL
        conditions.append('"cast" LIKE ?')
        values.append(f'%{filters["cast"]}%')

    if filters.get('imdb_rating'):
        # >= means "at least this rating" — not an exact match
        conditions.append('imdb_rating >= ?')
        values.append(filters['imdb_rating'])

    if filters.get('year_min'):
        conditions.append('year >= ?')
        values.append(filters['year_min'])

    if filters.get('year_max'):
        conditions.append('year <= ?')
        values.append(filters['year_max'])

    # always select the same specific columns — never use SELECT *
    base = 'SELECT title, year, genres, runtime_mins, type, number_of_seasons, number_of_episodes, imdb_rating, directors, imdb_id, "cast", poster_path FROM media'

    if conditions:
        # join all conditions with AND e.g. "type = ? AND genres LIKE ? AND imdb_rating >= ?"
        base += ' WHERE ' + ' AND '.join(conditions)

    conn = get_connection()
    cursor = conn.cursor()
    # pass values as a tuple — the ? placeholders are replaced in order
    rows = cursor.execute(base, values).fetchall()
    conn.close()

    return rows
