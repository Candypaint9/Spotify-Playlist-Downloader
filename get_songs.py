import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import math

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


auth_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

limit = 100

def makeFolder(playlist_link, path):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    results = sp.user_playlist(user = None, playlist_id=playlist_URI, fields="name")
    playlist_name = results["name"]

    path += playlist_name

    if os.path.exists(path) == False:
        os.mkdir(path)

    return path


def getSongs(playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    offset = 0
    songs = []

    while True:
        
        results = sp.playlist_tracks(playlist_id=playlist_URI, offset=offset, limit=limit)

        for track in results['items']:
            song = {}

            track = track["track"]

            song["track_name"] = track["name"]
            song["img_url"] = track["album"]["images"][0]["url"]
            song["album_name"] = track["album"]["name"]
            song["track_length"] = math.ceil(track["duration_ms"] / 1000)
            song["artists"] = ""
            for artist in track["artists"]:
                song["artists"] += artist["name"] + "; "
            song["artists"] = song["artists"][:-2]


            songs.append(song)

        offset += limit
        next = results['next']
        if next is None:
            break

    return songs