from datetime import timedelta
import os
from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slicerServer.settings')

app = Celery('slicerServer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'say-hello-every-sec': {
        'task': 'order.tasks.say_hello',
        'schedule': timedelta(seconds=1),
        'args':(),
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')