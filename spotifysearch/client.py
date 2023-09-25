
# THIS FILE IS RESPONSABLE FOR DEALING WITH THE CLIENT

from .classes import Authenticator, Results
from . import calls


class Client:

    def __init__(self, client_id, client_secret):
        self.auth = Authenticator(client_id, client_secret)


    def search(self, keywords:str, *, types:list = ['track'], filters:dict = {}, 
    market:str = None, limit:int = None, offset:int = None) -> Results:        
        access_token = self.auth.get_acess_token()
        args = (keywords, types, filters, market, limit, offset)
        response = calls.call_search(access_token, args)
        return Results(response.json())
