from main import settings

import requests

def url_join(*args):
    """
    Combine parts of url to always have slashes between and a trailing slash 
    at the end.
    """
    arglist = list(args)
    if arglist[-1] != '/':
        arglist.append('/')
    return "/".join(arg.strip("/") for arg in arglist)

def _delete_request(uri, headers):
    response = requests.delete(
        url_join(settings.TEST_BASE_URL, uri),
        headers=headers,
    )
    return response

def _get_request(uri, headers=None):
    response = requests.get(
        url_join(settings.TEST_BASE_URL, uri),
        headers=headers,
    )
    return response

def _post_request(uri, headers):
    response = requests.post(
        url_join(settings.TEST_BASE_URL, uri),
        headers,
    )
    return response

def _put_request(uri, headers):
    response = requests.put(
        url_join(settings.TEST_BASE_URL, uri),
        headers,
    )
    return response