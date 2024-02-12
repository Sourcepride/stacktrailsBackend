from utils.getenv import env
import gzip


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URI", "redis://127.0.0.1:6379") + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.gzip.GzipCompressor",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}


DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
DJANGO_REDIS_LOGGER = "django"
