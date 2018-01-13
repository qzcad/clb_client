from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cluster_client.settings')

broker_host = os.environ['BROKER_HOST']
broker_port = os.environ['BROKER_PORT']
broker_user = os.environ['BROKER_USER']
broker_pass = os.environ['BROKER_PASS']

app = Celery('cluster_client',
             broker='amqp://{}:{}@{}:{}'.format(broker_user, broker_pass,
                                                broker_host, broker_port),
             backend='rpc://')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
