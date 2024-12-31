import psycopg
from celery import shared_task
from psycopg.rows import dict_row


from conf import settings
from extract import extract_data
from load import load_data
from logger import logger
from transform import transform_data

dsl = {
    'dbname': settings.postgres_db,
    'user': settings.postgres_user,
    'password': settings.postgres_password,
    'host': settings.db_host,
    'port': settings.db_port,
}

@shared_task
def main():
    """
    Load data from Porstgres in Elasticsearch.
    """
    pg_conn = psycopg.connect(
        **dsl,
        row_factory=dict_row,
    )
    pg_curs = pg_conn.cursor()
    logger.info('Start load data.')
    extract = extract_data(pg_curs)
    transform = transform_data(extract)
    load_data(data=transform)
    logger.info('End load data.')


if __name__ == '__main__':
    logger.info('Start load data.')
    try:
        main()
    except Exception as e:
        logger.exception(e)
