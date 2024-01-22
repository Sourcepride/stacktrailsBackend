from stacktrails.config.base import BASE_DIR


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{levelname} {message}", "style": "{"},
        "standard": {
            "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "simple",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "WARNING",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/django.log",
            "maxBytes": (1024 * 30),
            "backupCount": 3,
        },
        "celery": {
            "level": "WARNING",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/celery.log",
            "maxBytes": (1024 * 30),
            "backupCount": 3,
            "mode": 'a'
        },
        "mail_admins": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "include_html": True,
        },
    },
    "loggers": {
        "celery": {
            "handlers": ["mail_admins", "celery"],
            "level": "WARNING",
            "propagate": False,
        },
        "django": {
            "handlers": ["mail_admins", "file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
