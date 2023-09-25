
# THIS FILE IS RESPONSABLE FOR THE CONSTRUCTION OF MANY OBJECTS

from . import classes


def get_available_markets(data):
    try:
        return data['available_markets']
    except KeyError:
        return None


# BASE ARGUMENTS FOR ALL CLASSES
def base_arguments(data):
    arguments = dict(
        data = data,
        type = data['type'],
        name = data['name'],
        url = data['external_urls']['spotify'],
        id  = data['id']
    )
    return arguments


# BASE ARGUMENTS FOR TRACK-LIKE CLASSES
def track_base_arguments(data):
    arguments = dict(
        explicit = data['explicit'],
        duration_ms = data['duration_ms']
    )
    return arguments


def artist(data):
    return classes.Artist(**base_arguments(data))


def track(data):
    base = base_arguments(data)
    track_base = track_base_arguments(data)

    arguments = dict(
        preview = data['preview_url'],
        artists = [artist(artist_data) for artist_data in data['artists']],
        album = album(data['album']),
        available_markets = get_available_markets(data),
        disc_number = data['disc_number'],
        popularity = data['popularity']
    )
    return classes.Track(**{**base, **track_base, **arguments})


def album(data):
    base = base_arguments(data)

    arguments = dict(
        images = [classes.AlbumCover(image['width'], image['height'], image['url']) for image in data['images']],
        artists = [artist(artist_data) for artist_data in data['artists']],
        available_markets = get_available_markets(data),
        release_date = data['release_date'],
        total_tracks = data['total_tracks']
    )
    return classes.Album(**{**base, **arguments})


def episode(data):
    base = base_arguments(data)
    track_base = track_base_arguments(data)

    arguments = dict(
        preview = data['audio_preview_url'],
        description = data['description'],
        html_description = data['html_description'],
        images = data['images'],
        language = data['language'],
        languages = data['languages'],
        release_date = data['release_date']
    )
    return classes.Episode(**{**base, **track_base, **arguments})
