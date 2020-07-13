from __future__ import absolute_import, unicode_literals
from celery import Celery
import json
import os
from django.conf import settings

#default django setting file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('FileServer', broker=settings.BROKER_URL)
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Seoul',
    enable_utc=True
)

#set celery keyword prefix to 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task
def add_new(jsonData):
    filename = os.path.join(settings.BASE_DIR, "setup/update_info.json")
    print(jsonData)
    with open(filename, "w") as json_file:
        json.dump(jsonData, json_file)
    return jsonData

