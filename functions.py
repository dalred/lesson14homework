import sqlite3

def connection_to_database(query, db):
    with sqlite3.connect(db) as connection:
        cur = connection.cursor()
        cur.row_factory = sqlite3.Row
        try:
            result = cur.execute(query)
            result = result.fetchall()
            result = [dict(ix) for ix in result]
            if len(result) > 0:
                #json.dumps(result, ensure_ascii=False) - решил отказаться от этого варианта
                return result
            else:
                return 'Нет данных по запросу!'
        except sqlite3.Error as er:
            return 'SQLite error: %s' % (' '.join(er.args))


