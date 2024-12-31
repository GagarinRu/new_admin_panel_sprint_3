import psycopg
import redis

from conf import settings
from constants import TABLES
from logger import logger
from storage import State


def person_ids(pg_conn: psycopg.Cursor, model, state):
    """
        Retrieves a list of person IDs and their corresponding last modified dates.

        :param pg_conn: A PostgreSQL connection object.
        :param model (str): The name of the model (e.g., 'person', 'genre').
        :param tate (int): The last known state of the model.

        :return: Tuple: A tuple containing two lists: person IDs and their last modified dates.
    """
    list_id = []
    list_last_date = []
    pg_conn.execute(
        f'SELECT id, modified FROM content.{model} '
        f"WHERE modified > '{state}' ORDER BY modified LIMIT 100;"
    )
    for value in pg_conn.fetchall():
        id, modified = str(value['id']), value['modified']
        list_id.append(id)
        list_last_date.append(modified)
    list_id = tuple(list_id)
    list_last_date = tuple(list_last_date)
    return list_id, list_last_date

def film_ids(pg_conn: psycopg.Cursor, model, ids):
    """
        Retrieves a list of film IDs related to the given person IDs.

        :param pg_conn: A PostgreSQL connection object.
        :param model (str): The name of the model (e.g., 'person', 'genre').
        :param ids (Tuple): A tuple of person IDs.

        :return: Tuple: A tuple of film IDs.
    """
    list_id = []
    pg_conn.execute(
        f'SELECT fw.id, fw.modified FROM content.film_work fw '
        f'LEFT JOIN content.{model}_film_work pfw ON pfw.film_work_id = fw.id '
        f'WHERE pfw.person_id  IN {ids} ORDER BY fw.modified LIMIT 100;'
    )
    for model in pg_conn.fetchall():
        ids = str(model["id"])
        list_id.append(ids)
    list_id = tuple(list_id)
    return list_id

def film_information(pg_conn: psycopg.Cursor, id):
    """
        Retrieves detailed information about the given film IDs.

        :param pg_conn: A PostgreSQL connection object.
        :param ids: A tuple of film IDs.

        :return: A dictionary containing detailed information about the films.
        """
    pg_conn.execute(
        'SELECT fw.id, fw.title, fw.description, fw.rating, fw.type, '
        'fw.created, fw.modified, array_agg(DISTINCT g.name) AS genres,'
         'COALESCE( json_agg(DISTINCT jsonb_build_object( '
        "'person_role', pfw.role, 'person_id', p.id, 'person_name', p.full_name)) "
        "FILTER (WHERE p.id IS NOT NULL), '[]') AS persons "
        'FROM content.film_work fw '
        'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id '
        'LEFT JOIN content.person p ON p.id = pfw.person_id '
        'LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id '
        'LEFT JOIN content.genre g ON g.id = gfw.genre_id '
        f' WHERE fw.id IN {id} GROUP BY fw.id ORDER BY fw.modified;'
    )
    data = pg_conn.fetchall()
    return data

def extract_data(pg_conn: psycopg.Cursor):
    """
    Extracts data from the database using the given PostgreSQL connection.

    :param pg_conn: A PostgreSQL connection object.

    :return: The extracted data.
    """
    logger.info('Start exctract data.')
    for model, name in TABLES.items():
        storage = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db
        )
        state = State(storage)
        id, last_date = person_ids(
            pg_conn,
            model,
            state.get_state(f'{name}_last_date')
        )
        if id == ():
            return []
        state.set_state(f'{name}_last_date', last_date[-1])
        if model in ['person', 'genre']:
            film_id = film_ids(pg_conn, model, id)
            return film_information(film_id)
        return film_information(pg_conn, id)
    pg_conn.close()
    logger.info('The extracted data.')
