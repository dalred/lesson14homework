from flask import Flask, jsonify
from models import Db_query

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
query = Db_query("database/netflix.db")

@app.route("/")
def page():
    return jsonify(query.get_actors('Rose McIver', 'Ben Lamb'))

@app.route("/<name>")
def page_name(name):
    return jsonify(query.get_film(name))

@app.route("/movie/<year>")
def page_year(year):
    return jsonify(query.get_year(year))

@app.route("/rating/<rating>")
def age_rating(rating):
    return jsonify(query.get_rating(rating))

if __name__ == '__main__':
    app.run('127.0.0.1', 8000)

