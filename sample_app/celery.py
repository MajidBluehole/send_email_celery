from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sample_app.settings')

app = Celery('sample_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.broker_connection_retry_on_startup = True


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()