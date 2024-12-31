from backoff import backoff
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from conf import settings
from logger import logger


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10)
def load_data(data):
    """
       Load data into Elasticsearch.

       This function attempts to connect to an Elasticsearch server and load the provided
       data into an index named "movies". If the data is empty, a log message is printed
       and the function returns without attempting to load anything. The function uses
       the `backoff` library to implement an exponential backoff retry mechanism in case
       of temporary connection failures.

       :param data: A list of dictionaries, where each dictionary is a document
        to upload to Elasticsearch. Each document must contain an "id" key.
       :return:- None
       :backoff:If connection to Elasticsearch fails after the maximum number of retries.

       """
    client = Elasticsearch(f'http://{settings.elastic_host}:{settings.elastic_port}')
    if data == []:
        logger.info('There is no data to download.')
        return
    data_es = [{'_id': value['id'], '_index': "movies", '_source': value} for value in data]
    bulk(client, data_es)
    logger.info('The download to Elasticsearch was successful.')