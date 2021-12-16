import sqlite3

def connection_to_database(query, db):
    with sqlite3.connect(db) as connection:
        cur = connection.cursor()
        try:
            result = cur.execute(query)
            result = list(result.fetchall())
            return result
        except sqlite3.Error as er:
            return 'SQLite error: %s' % (' '.join(er.args))


