import json
import sys
import re
import os
import lyrics
import random
from pprint import pprint

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

emojis = ''

with open(os.path.join(__location__, 'emojis.json')) as emojis_file:
    emojis = json.load(emojis_file)


def get_tweet_text():

    song_info = None

    while song_info == None:
        try:
            song_info = lyrics.get_lyrics()
        except Exception as e:
            print('No lyrics found, retrying')
            continue

    artist = song_info[0]
    song_title = song_info[1]
    song_lyrics = song_info[2]


    translated_lyrics = None
    if has_replaceable_words(song_lyrics):
        translated_lyrics = translate(song_lyrics)
    else:
        print('Song has no replaceable lyrics')
        sys.exit()

    artist_and_title = "\n" + artist + " - " + song_title
    tweetable_text = get_tweetable_lyrics(artist_and_title, translated_lyrics)
    return tweetable_text + artist_and_title


def get_matched_emojis(word):
    matched_emojis = []
    for emoji in emojis.items():
        keywords = emoji[1]['keywords']
        for keyword in keywords:
            if keyword == word:
                matched_emojis.append(emoji)
            else:
                plural1 = keyword + 's'
                plural2 = keyword + 'es'
                if word == plural1 or word == plural2:
                    matched_emojis.append(pluralize_emoji(emoji))

    return matched_emojis


def pluralize_emoji(emoji):
    dummy_emoji = ('dummy_code', {'char': 'dummy_char'})
    dummy_emoji[1]['char'] = emoji[1]['char'] + emoji[1]['char']
    return dummy_emoji


def has_replaceable_words(text):
    for word in text.split():
        matches = get_matched_emojis(word)
        if matches: # list is not empty, there is at least one replaceable word
            return True

    return False


def translate(text):
    temp_lyrics = text
    for word in re.split(r'[ \n\?,]', text):
        word = word.lower()
        matches = get_matched_emojis(word)

        if matches:
            random_emoji = random.choice(matches)
            temp_lyrics = re.sub(r'\b'+word+r'\b', random_emoji[1]['char'], temp_lyrics, flags=re.I)
    return temp_lyrics



def get_tweetable_lyrics(artist_and_title, song_lyrics):
    song_info_len = len(artist_and_title)
    remaining_chars_count = 140 - song_info_len

    texts_under_char_limit = []
    text_buffer = []

    for line in song_lyrics.split('\n'):
        # Try to append the current line until there is enough space
        text_buffer.append(line)
        while not is_below_char_limit(text_buffer, remaining_chars_count):
            # Exceeding char limit, delete oldest added line and try again
            text_buffer.pop(0)
        # Text is now below char limit, add to list of possible tweets
        joined_text = '\n'.join(text_buffer)
        texts_under_char_limit.append(joined_text)

    possible_tweets = []
    minimum_emoji_amount = 6
    for index, tweet in enumerate(texts_under_char_limit):
        emoji_count = get_emoji_count(tweet)
        if emoji_count > minimum_emoji_amount:
            possible_tweets.append(tweet)
    return random.choice(possible_tweets)

def get_emoji_count(text):
    emoji_count = 0
    for char in text:
        for emoji in emojis.items():
            if char == emoji[1]['char']:
                emoji_count += 1
    return emoji_count


def is_below_char_limit(text_list, remaining_chars_count):
    joined_text = '\n'.join(text_list)
    if len(joined_text) < remaining_chars_count:
        return True
    return False


if __name__ == '__main__':
    get_tweet_text()
