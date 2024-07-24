from __future__ import absolute_import, unicode_literals
import os
from config_celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books_reader.settings')

app = Celery('books_reader')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



