import json
import sys
import os
import pylast
from secrets import *

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

def get():
    with open(os.path.join(__location__, 'artists.json')) as artists_file:
        return json.load(artists_file)


def put(new_artists, existing_artists):
    for new in new_artists:
        existing_artists[new] = {}
    with open(os.path.join(__location__, 'artists.json'), mode='w') as new_artists_file:
        json.dump(obj=existing_artists, fp=new_artists_file, sort_keys=True)


def put_similar(reference_artist, existing_artists):
    password_hash = pylast.md5(LF_PASSWORD)
    network = pylast.LastFMNetwork(api_key=LF_API_KEY, api_secret=LF_SHARED_SECRET,
                                   username=LF_USERNAME, password_hash=password_hash)

    artist_obj = network.get_artist(reference_artist)
    print('Got: ' + str(artist_obj))
    similar_artists = artist_obj.get_similar()

    for name, props in similar_artists:
        print('Adding: ' + str(name))
        existing_artists[str(name)] = {}
    with open(os.path.join(__location__, 'artists.json'), mode='w') as new_artists_file:
        json.dump(obj=existing_artists, fp=new_artists_file,
                  sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':

    all_artists = get()
    if len(sys.argv) != 1:
        if sys.argv[1] == '-a':
            put(sys.argv[2:], all_artists)
        elif sys.argv[1] == '-s':
            put_similar(sys.argv[2], all_artists)
        else:
            print('Usage: python3.5 artists.py -s artist_name')
    else:
        print('Usage: python3.5 artists.py -s artist_name')
