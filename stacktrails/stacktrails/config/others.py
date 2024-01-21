from utils.getenv import env
import json

FACILITY_IMAGE_PATH = "images/facility/"
DEFAULT_FROM_EMAIL = "no-reply@nuodal.com"
DYNAMIC_HOST_RESOLVER_FUNC = "stacktrails.filter_domain.filter_domain"
DEFAULT_ORIGINS = env("DEFAULT_ORIGINS", "[]")
DYNAMIC_HOST_DEFAULT_HOSTS = [
    "testserver",
    env("SERVER_IP", ""),
    env("SITE_DOMAIN", ""),
    env("SITE_SUB", ""),
    *json.loads(env("OTHER_DOMAINS", "[]")),
]


SCHEDULER_THRESH = 2
