from utils.getenv import env


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "PORT": 5432,
        "HOST": env("DB_HOST"),
        "TEST": {
            "NAME": env("DB_NAME")
        }
    },
}

import os

print("{============================}",  env("DB_NAME"),  os.getenv("DB_NAME"),  os.environ.get("DB_NAME"), "\n\n\n\n\n\n",  os.environ)
