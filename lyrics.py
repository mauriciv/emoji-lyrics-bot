import pylast
import random
from pprint import pprint
from secrets import *
from PyLyrics import *

def get_lyrics():
    password_hash = pylast.md5(LF_PASSWORD)
    network = pylast.LastFMNetwork(api_key = LF_API_KEY, api_secret = LF_SHARED_SECRET,
                    username = LF_USERNAME, password_hash = password_hash)
    top_artists = network.get_top_artists()
    random_artist = network.get_artist(random.choice(top_artists).item)


    top_albums = random_artist.get_top_albums()
    random_album = random.choice(top_albums).item

    tracks = random_album.get_tracks()

    random_track = ''
    if tracks != []:
        random_track = random.choice(tracks).get_title()

    artist_name = str(random_artist.get_name())

    if random_track != '':
        lyrics = PyLyrics.getLyrics(artist_name, random_track)
        return (artist_name, random_track, lyrics)
