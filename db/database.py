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
        imdb_id TEXT NOT NULL,
        UNIQUE(name, imdb_id))
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


def get_unique_values(column):
    """Returns a sorted list of unique values from a comma-separated column"""
    conn = get_connection()
    cursor = conn.cursor()

    # only fetch the requested column — no need to load all columns
    # use quoted column for SQL, but strip quotes for dictionary lookup
    sql_column = f'"{column}"'  # always wrap in double quotes for SQL safety
    rows = cursor.execute(f'SELECT {sql_column} FROM media').fetchall()

    values = set()  # a set automatically ignores duplicates

    for row in rows:
        row_dict = dict(row)  # convert sqlite3.Row to a regular dictionary
        if row_dict[column]:  # skip rows where values is None
            for value in row_dict[column].split(', '):  # split "Comedy, Romance" into ["Comedy", "Romance"]
                values.add(value)  # add each individual value to the set

    conn.close()

    return sorted(values)  # convert set to a sorted list


def get_collection_names():
    """Returns all saved collection names"""
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute('SELECT DISTINCT name FROM collections').fetchall()
    names = list()
    for row in rows:
        names.append(row['name'])
    conn.close()
    return sorted(names)


def save_collection(name, imdb_ids):
    """Saves a list of imdb_ids under a collection name. Returns True on success, False on failure."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for imdb_id in imdb_ids:
            cursor.execute('INSERT OR IGNORE INTO collections (name, imdb_id) VALUES (?, ?)', (name, imdb_id))
        conn.commit()
        return True
    except Exception as e:
        print(f'Error saving collection: {e}')
        return False
    finally:
        conn.close()


def delete_collection(name):
    """Deletes all entries for a given collection name. Returns True on success, False on failure."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM collections WHERE name = ?', [name])
        conn.commit()
        return True
    except Exception as e:
        print(f'Error deleting collection: {e}')
        return False
    finally:
        conn.close()


def remove_from_collection(name, imdb_id):
    """Removes one specific row matching both the collection name and the imdb_id"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM collections WHERE name = ? AND imdb_id = ?', [name, imdb_id])
        conn.commit()
        return True
    except Exception as e:
        print(f'Error deleting collection item: {e}')
        return False
    finally:
        conn.close()
    

# save_collection('Favourites', ['tt12042730'])

# print(get_collection_names())

# print(get_unique_values('genres'))
# print(get_unique_values('cast'))
# print(get_unique_values('directors'))

