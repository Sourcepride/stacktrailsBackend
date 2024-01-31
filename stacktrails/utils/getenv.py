import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# helper function
def env(key, default=None):
    value = os.getenv(key)
    if value is not None:
        return value
    return default
