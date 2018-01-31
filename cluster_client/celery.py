from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cluster_client.settings')

broker_host = os.environ['BROKER_HOST']
broker_port = os.environ['BROKER_PORT']
db_number = os.environ['DB_NUMBER']

broker_url = 'redis://{host}:{port}/{db_number}'.format(
    host=broker_host,
    port=broker_port,
    db_number=db_number
)

app = Celery('cluster_client', broker=broker_url)

app.conf.result_backend = broker_url

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
