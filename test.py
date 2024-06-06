from pytube import YouTube
from pytube import Search
import os
from dotenv import load_dotenv
import spotipy
import spotipy.oauth2 as oauth2

def getmp4(track_name, artist_name):
    result = Search(track_name + " " + artist_name + " lyrics").results[0]

    destination = "./Temp"

    for stream in result.streams.filter(only_audio=True):
        try:
            video = stream
            file = video.download(output_path=destination)
            return file
        
        except Exception as e:
            continue




load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

credentials = oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)


results = spotify.user_playlist(user="8qaf6rikv94dw8h5adx33eg2y", fields='name', playlist_id="https://open.spotify.com/playlist/7aM38uIRZcGlKHWx6x2y9v?si=yoC6FnIrRd22X4fXLV9kwA&pt=72e55f8c9c9589209b7c792baf953504&pi=ZUn_T-HcQtWGu".split("/")[-1].split("?")[0])



#getmp4('Mayonaka no Door / Stay With Me',  'Miki Matsubara')