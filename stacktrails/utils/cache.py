from os import getenv
from datetime import timedelta
import redis

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class RedisCacheController:
    def __init__(self, db=0) -> None:
        self._pool = redis.ConnectionPool(
            host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), db=db
        )
        self._redis = redis.Redis(connection_pool=self._pool)

    def key_exists(self, key: str):
        return self._redis.exists(key)

    def get_value(self, key: str):
        return self._redis.get(key).decode("utf-8")

    def set_value(self, key: str, value: str, **kwargs):
        return self.set_str_val(key, value, **kwargs)

    def delete_val(self, key: str):
        resp = self._redis.delete(key)
        if resp == 1:
            return "OK"
        return "Not found"

    def set_str_val(self, key: str, value: str, exp_mins: int = (60 * 24)):
        if not isinstance(value, str):
            raise TypeError("has to be a string value")
        if not isinstance(key, str):
            raise TypeError("key has to be of type string")
        if not isinstance(exp_mins, int):
            raise TypeError("exp has to be of type int")

        self._redis.setex(key, timedelta(minutes=exp_mins), value)
        return "OK"

    def use_pipe(self, callback):
        with self._redis.pipeline() as pipe:
            callback(pipe)


class CacheKeyHandlers:  # TODO:bad name should probably change
    """handlers registered here returns keys that will be used to identify a unique view
    to prevent key clash... we solve this by prefixing unique registered handler names
    to keys returned
    """

    registered_handlers = {
        "facility_search": lambda x: x.query_params.get("q", "")
        + str(x.query_params.get("page", 1)),
    }

    def get_registered_handlers(self):
        return self.registered_handlers.keys()

    def get_cache_key(self, name, request):
        handler = self.registered_handlers[name]
        if not callable(handler):
            raise TypeError("handler must be callable")
        value = handler(request)
        if not isinstance(value, str):
            raise TypeError("handler return value must be of type string")
        return name + value
