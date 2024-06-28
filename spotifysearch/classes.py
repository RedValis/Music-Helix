
# THIS FILE IS RESPONSABLE FOR MANY CLASS DECLARATIONS

import json
import math
from base64 import b64encode
from urllib.request import urlretrieve
from . import constructor
from . import calls


# AUTHENTICATION AND TOKENS
class Authenticator:

    def __init__(self, client_id:str, client_secret:str):
        self.credentials = self.encode_credentials(client_id, client_secret)
    

    def encode_credentials(self, client_id, client_secret):
        credentials = f'{client_id}:{client_secret}'
        encoded_credentials = b64encode(credentials.encode('utf-8'))
        return str(encoded_credentials, 'utf-8')


    def get_acess_token(self):
        response = calls.call_acess_token(self.credentials)
        return response.json()['access_token']


# OBJECTS

# Base class for all classes
class Base: 
    
    def __init__(self, data, type, name, url, id):
        self.data = data
        self.type = type
        self.name = name
        self.url = url
        self.id = id
    

    def export_json(self, path:str):
        file = open(path, 'w')
        json.dump(self.data, file, indent=4)
        file.close()


# Base class for track-like objects
class TrackBase(Base): 
    
    def __init__(self, data, type, name, url, id, explicit, duration_ms):
        super().__init__(data, type, name, url, id)
        self.explicit = explicit
        self.duration_ms = duration_ms
    

    def get_formatted_duration(self) -> dict:
        
        duration_in_seconds = self.duration_ms / 1000
        hours = 0
        mins = math.floor(duration_in_seconds // 60)

        if mins >= 60:
            hours = math.floor(mins // 60)
            mins = math.floor(mins % 60)
        
        secs = math.floor(duration_in_seconds % 60)

        return {'hours':hours, 'minutes':mins, 'seconds':secs}
    

    def get_string_duration(self) -> str:
     
        duration = self.get_formatted_duration()
        format = self.__format_duration
        
        hours = format(str(duration['hours']))
        mins = format(str(duration['minutes']))
        secs = format(str(duration['seconds']))       
        
        if int(hours):
            return f'{hours}:{mins}:{secs}'
        else:
            return f'{mins}:{secs}'


    def __format_duration(self, value:str):
        if len(value) < 2:
            return ('0' + value)
        else: return value


class Artist(Base):

    def __init__(self, data:dict, type:str, name:str, url:str, id:str):
        super().__init__(data, type, name, url, id)


class AlbumCover:

    def __init__(self, width, height, url):
        self.width = width
        self.height = height
        self.url = url
    

    def export_image(self, path):
        urlretrieve(self.url, path)


class Album(Base):

    def __init__(self, data:dict, type:str, name:str, url:str, id:str, 
    images:list, artists:list, available_markets:list, release_date:str, total_tracks:int):
        
        super().__init__(data, type, name, url, id)
        self.images = images
        self.artists = artists
        self.available_markets = available_markets
        self.release_date = release_date
        self.total_tracks = total_tracks
        

class TrackPreview:

    def __init__(self, url):
        self.url = url
    

    def export_audio(self, path):
        urlretrieve(self.url, path)


class Track(TrackBase):

    def __init__(self, data:dict, type:str, name:str, url:str, id:str, explicit:bool,
    duration_ms:int, preview:TrackPreview, artists:list, album:Album, available_markets:list, 
    disc_number:int, popularity:int):
        
        super().__init__(data, type, name, url, id, explicit, duration_ms)
        self.preview = preview
        self.artists = artists
        self.album = album
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.popularity = popularity


class Episode(TrackBase):

    def __init__(self, data:dict, type:str, name:str, url:str, id:str, 
    explicit:bool,  duration_ms:int, preview:str, description:str, html_description:str,
    images:list, language:str, languages:list, release_date:str):
        
        super().__init__(data, type, name, url, id, explicit, duration_ms)
        self.preview = preview
        self.description = description
        self.html_description = html_description
        self.images = images
        self.language = language
        self.languages = languages
        self.release_date = release_date


# CLIENT OBJECTS
class Results(Base):

    def __init__(self, data):
        self.data = data
    

    def __get_items(self, type):     
        
        if type == 'artist':
            try:
                data = self.data['artists']['items']
                func = constructor.artist
            except KeyError:
                return []
        
        elif type == 'track':
            try:
                data = self.data['tracks']['items']
                func = constructor.track
            except KeyError:
                return []
        
        elif type == 'album':
            try:
                data = self.data['albums']['items']
                func = constructor.album
            except KeyError:
                return []
        
        elif type == 'episode':
            try:
                data = self.data['episodes']['items']
                func = constructor.episode
            except KeyError:
                return [] 
        
        return [func(item) for item in data]


    def get_tracks(self) -> list:
        return self.__get_items('track')
    

    def get_artists(self) -> list:
        return self.__get_items('artist')
    

    def get_albums(self) -> list:
        return self.__get_items('album')


    def get_episodes(self) -> list:
        return self.__get_items('episode')
