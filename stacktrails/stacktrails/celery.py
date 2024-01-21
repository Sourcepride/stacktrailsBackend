import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kwick_access.settings")

app = Celery("kwick_access")

app.config_from_object("django.conf:settings", namespace="CELERY")
if settings.DEBUG:
    app.conf.task_default_queue = "cpu"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    from django.conf import settings

    dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
