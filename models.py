from functions import connection_to_database


class Db_query:
    def __init__(self, db):
        self.db = db
    #Шаг 1
    def get_film(self, name):
        query = f"""
                            Select title, country, listed_in as genre,release_year, description
                            From netflix
                            where title='{name}' and type='Movie' ORDER BY release_year DESC"""
        result = connection_to_database(query, self.db)
        if len(result) > 0:
            titles = ['title', 'country', 'genre', 'release_year', 'description']
            data_dict = dict(zip(titles, result[0]))
            return data_dict
        else:
            return 'Нет фильма по данному запросу!'
    #Шаг 2
    def get_year(self, year) -> list:
        titles = ['title', 'release_year']
        query = f"""
                        Select title, release_year
                        From netflix
                        where type='Movie' and release_year <={year} ORDER BY release_year DESC LIMIT 100"""
        result = connection_to_database(query, self.db)
        data_dict = [dict(zip(titles, i)) for i in result]
        return data_dict
    #Шаг 3
    def get_rating(self, rating):
        query = ''
        titles = ['title', 'rating', 'description']
        if rating == 'children':
            query = f"""
                                    Select title, rating, description
                                    From netflix
                                    where rating='G'"""
        if rating == 'family':
            query = f"""
                                           Select title, rating, description
                                           From netflix
                                           where rating='PG' or rating='PG-13'"""
        if rating == 'adult':
            query = f"""
                                            Select title, rating, description
                                            From netflix
                                            where rating='R' or rating='NC-17'"""
        result = connection_to_database(query, self.db)
        if len(result) > 0:
            data_dict = [dict(zip(titles, i)) for i in result]
            return data_dict
        else:
            return "Нет фильма по данному запросу!"
    #Шаг 4
    def top_genre(self, name) -> list:
        query = f"""
                            Select title, description
                            From netflix
                            where listed_in like'%{name}%' and type='Movie' ORDER BY release_year DESC Limit 10"""
        result = connection_to_database(query, self.db)
        titles = ['title', 'description']
        data_dict = [dict(zip(titles, i)) for i in result]
        return data_dict

    # Rose McIver Ben Lamb
    #Здесь нужно будет остановиться на ДЗ, и так как я сдаю до,
    #Мне простительно) но по факту чтобы сделать группировку,
    #Нужно разбить строку в SQL.
    def get_actors(self, first, second) -> list:
        query = f"""
                            Select "cast"
                            From netflix
                            where "cast" like'%{first}%' and "cast" like'%{second}%'
        """
        result = connection_to_database(query, self.db)
        dict_arr = []
        dict_lst = [item[0].split(', ') for item in result]
        for item in dict_lst:
            for jitem in item:
                if jitem != first and jitem != second:
                    dict_arr.append(jitem)
        data = []
        result = {i: dict_arr.count(i) for i in dict_arr if dict_arr.count(i) > 2}
        #По желанию
        for k, v in result.items():
            data.append({'actor': k, 'count': v})
        return data
    #Шаг 6 тип картины (фильм или сериал), год выпуска и ее жанр
    def get_picture(self, type_, year, genre) -> list:
        titles = ['title', 'description']
        query = f"""
                            Select title, description
                            From netflix
                            where type="{type_}" 
                            and release_year={year}
                            and listed_in like "%{genre}%"
        """
        result = connection_to_database(query, self.db)
        data_dict = [dict(zip(titles, i)) for i in result]
        return data_dict
