from get_songs import getSongs
from get_songs import makeFolder
from download import makeSong
import os
import warnings

warnings.filterwarnings("ignore")

playlist_link = input("Enter playlist link: ")

playlist_name = makeFolder(playlist_link)

print("Made Folder")

songs = getSongs(playlist_link)

print("Got Songs")

count = 0
total = len(songs)

for song in songs:
    name = song["artist_name"] + " - " + song["track_name"]
    
    bad_chars = [':', '!', "*", "/", "\\", "?", "|", "<", ">", '"']
    for i in bad_chars:
        name = name.replace(i, '')
    
    if os.path.exists("./" + playlist_name + "/" + name + ".mp3") == False:
        print(song['track_name'])
        try:
            makeSong(song, playlist_name)
        except Exception as e:
            print(e)
    count += 1

    print(str(count) + ' / ' + str(total))