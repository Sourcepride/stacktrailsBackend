from stacktrails.config.base import DEBUG
from utils.getenv import env

if not DEBUG:
    import re

    domain = re.compile(f"https://{env('SITE_DOMAIN')}")
    subs = re.compile(f"https://.*\.{env('SITE_DOMAIN')}")

    CORS_ALLOWED_ORIGIN_REGEXES = [domain, subs]
    SERVER_DOMAINS = [
        env("SERVER_IP"),
        env("SITE_DOMAIN"),
        env("SITE_SUB"),
    ]
else:
    SERVER_DOMAINS = []
    CORS_ALLOW_ALL_ORIGINS = True
