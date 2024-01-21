from utils.getenv import env

# CELERY
CELERY_BROKER_URL = env("BROKER_URL")
CELERY_RESULT_BACKEND = env("RESULT_BACKEND")
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_CREATE_MISSING_QUEUES = True
