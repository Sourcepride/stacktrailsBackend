# Application definition

THIRD_PARTIES = [
    "corsheaders",
    "rest_framework",
    "django_celery_beat",
    "dynamic_host",
]

PROJECT_APPS = [
    "account.apps.AccountConfig"
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTIES,
    *PROJECT_APPS,
]
