import json
from functools import wraps

from django.db import transaction
from rest_framework.response import Response

from .cache import CacheKeyHandlers


def ensure_atomic(view):
    @wraps(view)
    def atomic(*args, **kwargs):
        with transaction.atomic():
            return view(*args, **kwargs)

    return atomic