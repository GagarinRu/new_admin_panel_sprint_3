from celery.schedules import crontab

from conf import settings


broker_url = f'redis://{settings.redis_host}:{settings.redis_port}/{settings.celery_redis_db}'
result_backend = f'redis://{settings.redis_host}:{settings.redis_port}/{settings.celery_redis_db}'
include = ['main_tasks']
broker_connection_retry_on_startup = True
broker_connection_retry_on_startup = True
beat_schedule = {
    'update_es_every_five_minutes': {
        'task': 'main_tasks.main',
        'schedule': crontab(minute='*/5')
    },
}