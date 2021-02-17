from celery import Celery
from django_celery_beat.models import PeriodicTask, PeriodicTasks

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def say_hello():
    return "hello"