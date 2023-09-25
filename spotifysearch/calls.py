
# THIS FILE IS RESPONSABLE FOR API CALLS

from . import urlbuilder
from requests import get, post


def call_acess_token(credentials):
    endpoint = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type':'client_credentials'
    }
    headers = {
        'Authorization':f'Basic {credentials}'
    }
    return post(url=endpoint, data=data, headers=headers)


def call_search(acess_token, args):
    endpoint = urlbuilder.search_endpoint(*args)
    headers = {
        'Authorization':f'Bearer {acess_token}'
    }
    return get(url=endpoint, headers=headers)
