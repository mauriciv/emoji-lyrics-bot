import pylast
import random
import json
import os
from pprint import pprint
from my_secrets import *
from lyrics_extractor import SongLyrics
import sys

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def get_lyrics():
    password_hash = pylast.md5(LF_PASSWORD)
    network = pylast.LastFMNetwork(api_key=LF_API_KEY, api_secret=LF_SHARED_SECRET,
                                   username=LF_USERNAME, password_hash=password_hash)

    print('Getting artist.')

    artists_dict = None
    with open(os.path.join(__location__, 'artists.json')) as artists_file:
        artists_dict = json.load(artists_file)
    random_artist_name = random.choice(list(artists_dict.keys()))

    random_artist = network.get_artist(random_artist_name)
    print("Got: " + str(random_artist))

    print('Getting album')
    top_albums = random_artist.get_top_albums()
    random_album = random.choice(top_albums).item
    print("Got: " + str(random_album))

    print('Getting track')
    tracks = random_album.get_tracks()
    random_track = ''
    if tracks != []:
        random_track = random.choice(tracks).get_title()
    else:
        print('No tracks available.')

    artist_name = str(random_artist.get_name())

    extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)
    if random_track != '':
        print('Getting track lyrics.')
        data = extract_lyrics.get_lyrics(artist_name + ' ' + random_track)
        return (artist_name, random_track, data['lyrics'])
    else:
        print('No track found.')
