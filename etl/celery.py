from celery import Celery

import celeryconfig


app = Celery('celery')
app.config_from_object(celeryconfig, namespace='CELERY')
app.autodiscover_tasks()
app.conf.enable_utc = True

