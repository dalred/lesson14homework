import sqlite3
from flask import Flask, jsonify
import traceback
import sys


def connection_to_database(query):
    with sqlite3.connect("database/netflix.db") as connection:
        cur = connection.cursor()
        try:
            result = cur.execute(query)
            result = list(result.fetchall())
            return result
        except sqlite3.Error as er:
            return 'SQLite error: %s' % (' '.join(er.args))



# def get_actors(first: str, second: str):
#     sql = f"SELECT \"cast\" FROM netflix WHERE \"cast\" LIKE '%{first}%' AND \"cast\" LIKE '%{second}%'"
#     with sqlite3.connect("database/netflix.db") as cursor:
#         cursor = cursor.cursor()
#         cursor.execute(sql)
#         result_set = set()
#         for actors in cursor.fetchall():
#             if actors:
#                 data = set(actors[0].split(', '))
#                 data.remove(first)
#                 data.remove(second)
#                 result_set.update(data)
#
#         return sorted(result_set)
#
# print(get_actors('Rose McIver','Ben Lamb'))

def test(type,year,genre):
    titles = ['title', 'description']
    query = f"""
                        Select title, description
                        From netflix
                        where type="{type}" 
                        and release_year={year}
                        and listed_in like "%{genre}%"
    """
    result = connection_to_database(query)
    data_dict = [dict(zip(titles, i)) for i in result]
    print(data_dict)

