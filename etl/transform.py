from constants import ROLES
from logger import logger

def transform_data(data):
    """
        Converts the source data of movies into a format corresponding to certain constants.

        The `transform_data' function takes a list of movie data
        and converts it to a format defined by constants from the
        `constants.ROLES` module.A new dictionary with the transformed
        data is created for each movie in the list.
        Fields for the ID, title, description, rating, and genres
        of the movie are added to this dictionary.
        Also, for each director, actor, and screenwriter in the film,
        corresponding fields are created with their IDs and names.

        :param data: A list of dictionaries representing movies. Each dictionary
        contains information about the movie, including ID, title, description,
        rating, and genres.

        :return: A list of converted dictionaries, where each dictionary represents
        a movie with additional fields for directors, actors, and screenwriters.
        """
    logger.info('Start converts data.')
    if data == []:
        logger.info('data is null')
        return data
    else:
        list_data = []
        for film in data:
            transform_film = {
                'id': str(film['id']),
                'title': film['title'],
                'description': film['description'],
                'imdb_rating': film['rating'],
                'genres': film['genres'],
            }
            for role in ROLES:
                name = role.split('s',1)[0]
                if role in ('directors', 'actors', 'writers'):
                    transform_film[role] = [
                        {'id': person['person_id'], 'name': person['person_name']}
                        for person in film['persons']
                        if person['person_role'] == name
                    ]
                else:
                    transform_film[role] = [
                        person['person_name']
                        for person in film['persons']
                        if person['person_role'] == name
                    ]
            list_data.append(transform_film)
        logger.info('data is convert.')
        return list_data
