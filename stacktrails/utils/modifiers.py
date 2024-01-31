from functools import partial, update_wrapper

import requests


def make_request(
    url,
    method="get",
    headers=dict(),
    data=None,
):
    headers = {"Content-Type": "application/json", **headers}
    response = requests.request(method=method, url=url, data=data, headers=headers)
    if response.status_code >= 200 and response.status_code <= 399:
        return True, response.json()
    return False, response.json()


class staticOrClassMethod:
    """This descriptor class makes a class bound function accessible like a static function
    when accessed via the class and like a normal method when accessed via an object
    """

    def __init__(self, function):
        self.function = function
        update_wrapper(self, function)

    def __get__(self, obj, objtype=None):
        if obj:
            return partial(self.function, obj)
        elif objtype:
            return self.function

    def __set__(self):
        raise AttributeError("cannot access this attribute")
