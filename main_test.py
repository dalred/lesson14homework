from flask import Flask, jsonify
from test import connection_to_database

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


def top_genre(name)->dict:
    query = f"""
                        Select title, description
                        From netflix
                        where listed_in like'%{name}%' and type='Movie' ORDER BY release_year DESC Limit 10"""
    result = connection_to_database(query)
    titles = ['title', 'description']
    data_dict = [dict(zip(titles, i)) for i in result]
    return data_dict
def actors(first, second)->dict:
    query = f"""
                        Select "cast"
                        From netflix
                        where "cast" like'%{first}%' and "cast" like'%{second}%'
    """
    result = connection_to_database(query)
    dict_arr = []
    dict_lst = [item[0].split(', ') for item in result]
    for item in dict_lst:
        for jitem in item:
            if jitem != 'Rose McIver' and jitem != 'Ben Lamb':
                dict_arr.append(jitem)
    data = []
    result = {i: dict_arr.count(i) for i in dict_arr if dict_arr.count(i) > 2}
    for k, v in result.items():
        data.append({'actor': k, 'count': v})
    return data
def picture(type,year,genre)->dict:
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
    return data_dict
@app.route("/")
def main():
    return jsonify(picture('Movie',2021,'Comedies'))

@app.route("/<name>")
def page_name(name):
    query = f"""
                    Select title, country, listed_in as genre,release_year, description
                    From netflix
                    where title='{name}' and type='Movie' ORDER BY release_year DESC"""
    result = connection_to_database(query)
    if len(result) > 0:
        titles = ['title', 'country', 'genre', 'release_year', 'description']
        data_dict = dict(zip(titles, result[0]))
        return data_dict
    else:
        return 'Нет фильма по данному запросу!'


@app.route("/movie/<year>")
def page_year(year):
    titles = ['title', 'release_year']
    query = f"""
                Select title, release_year
                From netflix
                where type='Movie' and release_year <={year} ORDER BY release_year DESC LIMIT 100"""
    result = connection_to_database(query)
    data_dict = [dict(zip(titles, i)) for i in result]
    return jsonify(data_dict)

@app.route("/rating/children")
def rating_children():
    titles = ['title', 'rating', 'description']
    query = f"""
                        Select title, rating, description
                        From netflix
                        where rating='G'"""
    result = connection_to_database(query)
    data_dict = [dict(zip(titles, i)) for i in result]
    return jsonify(data_dict)

@app.route("/rating/family")
def rating_family():
    titles = ['title', 'rating', 'description']
    query = f"""
                        Select title, rating, description
                        From netflix
                        where rating='PG' or rating='PG-13'"""
    result = connection_to_database(query)
    data_dict = [dict(zip(titles, i)) for i in result]
    return jsonify(data_dict)


@app.route("/rating/adult")
def rating_adult():
    titles = ['title', 'rating', 'description']
    query = f"""
                        Select title, rating, description
                        From netflix
                        where rating='R' or rating='NC-17'"""
    result = connection_to_database(query)
    data_dict = [dict(zip(titles, i)) for i in result]
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run('127.0.0.1', 8000)
