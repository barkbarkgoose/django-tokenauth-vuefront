from main import settings

import requests

class MakeRequest:
    """
    class with static methods the help in making http requests
    """
    def _url_join(*args):
        """
        Combine parts of url to always have slashes between and a trailing slash 
        at the end.
        """
        arglist = list(args)
        if arglist[-1] != '/':
            arglist.append('/')
        return "/".join(arg.strip("/") for arg in arglist)

    def delete(uri, auth=None, headers=None, json=None):
        response = requests.delete(
            MakeRequest._url_join(settings.TEST_BASE_URL, uri),
            auth=auth,
            headers=headers,
            json=json,
        )
        return response

    def get(uri, auth=None, headers=None, json=None):
        response = requests.get(
            MakeRequest._url_join(settings.TEST_BASE_URL, uri),
            auth=auth,
            headers=headers,
            json=json,
        )
        return response

    def patch(uri, auth=None, headers=None, json=None):
        response = requests.patch(
            MakeRequest._url_join(settings.TEST_BASE_URL, uri),
            auth=auth,
            headers=headers,
            json=json,
        )
        return response

    def post(uri, auth=None, headers=None, json=None):
        response = requests.post(
            MakeRequest._url_join(settings.TEST_BASE_URL, uri),
            auth=auth,
            headers=headers,
            json=json,
        )
        return response

    def put(uri, auth=None, headers=None, json=None):
        response = requests.put(
            MakeRequest._url_join(settings.TEST_BASE_URL, uri),
            auth=auth,
            headers=headers,
            json=json,
        )
        return response