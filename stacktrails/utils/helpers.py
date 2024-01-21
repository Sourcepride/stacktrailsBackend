import os
import time
import json
from urllib.parse import urlsplit
from typing import Callable, Iterable, Set
from datetime import datetime, timedelta, timezone as pytimezone
from io import BytesIO
import base64
import uuid

from PIL import Image
import jwt
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.http.request import split_domain_port

"""NOTE:  most functions here are either pure functions or functions with almost no side effect and should remain that
way as they are imported all over the project
"""


def inmemory_wrapper(image, default_path: str):
    # TODO: find how to reduce get_mail_credentialssize of ImageFieldFile
    if (not image) or image == default_path or isinstance(image, ImageFieldFile):
        return image

    format_ = file_extention_from_name(image.url)
    image_file = resizeImage(image, width_size=200, format_=format_)
    return InMemoryUploadedFile(
        image_file,
        "ImageField",
        f"{image.name}",
        f"image/{format_}",
        image_file.tell(),
        None,
    )


def file_extention_from_name(name):
    str_array = name.split(".")
    if len(str_array) < 2:
        raise ValueError("invalid extension or file has no extension")
    return str_array[-1]


def resizeImage(image, width_size=200, format_: str = "jpeg"):
    file = Image.open(BytesIO(image))
    thumb_io = BytesIO()
    width, height = file.size
    format_ = "jpeg" if format_ == "jpg" else format_
    # keep aspect ratio
    file = file.resize([width_size, int((width_size * height) / width)])
    try:
        file.save(thumb_io, format=format_, quality=70)
    except ValueError:
        file = file.convert("RGB")
        file.save(thumb_io, format=format_, quality=70)

    # reset pointer to starting byte
    thumb_io.seek(0)
    return thumb_io


def encoded_uuid4_to_str():
    return base64.urlsafe_b64encode(str(uuid.uuid4()).encode()).decode("utf-8")


def generate_jwt_token(payload: dict, exp):
    secret = os.getnv("SECRET_KEY")
    payload = {**payload, "exp": exp}
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt_token(token: str, keys_expected: list = []):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
    except Exception as e:
        return {"error": e}, True

    # this way you are sure the decoded data is what you're expecting
    is_validated = validate_decoded_payload(keys_expected, payload)

    if not is_validated:
        return {"error": "expectation not found"}, True
    return payload, False


def validate_decoded_payload(expected_keys, payload):
    if not payload:
        return False

    if not expected_keys:
        return True

    run_checks = all(payload.get(key) for key in expected_keys)
    return run_checks


def construct_jwt_expiration_dict(num_of_hours_valid=1):
    return {
        "exp": datetime.now(tz=pytimezone.utc) + timedelta(hours=num_of_hours_valid),
        "iat": datetime.now(tz=pytimezone.utc),
    }


def slice_func(callable_, start=0, end=0):
    return callable_()[start:end]


def divide_by_unit(value, unit: int):
    return round((value / unit), 2)


def multiply_by_unit(value, unit: int):
    return int(value * unit)


# def get_profile_object(user):
#     return user.get_profile.profile_object


def get_or_default(obj, attr, default=None):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    return default


def get_unique(values: Iterable, func: Callable = None) -> Set:
    results = set()
    for value in values:
        value = func(value) if func else value
        if not isinstance(value, (list, tuple)):
            results.add(value)
            value = []
            continue
        results = set([*results, *value])
    return results


def is_in_default_hosts(host: str):
    default_origins = settings.DEFAULT_ORIGINS
    if not isinstance(default_origins, str):
        raise TypeError("value of allowed host must be a string")
    values = json.loads(default_origins)
    if not isinstance(values, list):
        raise TypeError("value expected must be a list")

    return host in values


def get_origin(request):
    if not request.META.get("HTTP_ORIGIN"):
        return

    hostname = urlsplit(request.META["HTTP_ORIGIN"]).hostname
    if hostname:
        return hostname
    return split_domain_port(request.META["HTTP_ORIGIN"])[0]


def call_again(function, *args, calls=1, wait=0.2, **kwargs):
    try:
        data = function(*args, **kwargs)
        return True, data
    except Exception as e:
        print(e)

        time.sleep(wait)
        if calls < 4:
            call_again(function, *args, calls=calls + 1, **kwargs)
        return False, {}
