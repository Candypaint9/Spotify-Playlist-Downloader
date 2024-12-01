from get_songs import getSongs
from get_songs import makeFolder
from download import makeSong
import os
import warnings
warnings.filterwarnings("ignore")

path = "C:/Users/advai/Music/"

playlist_link = input("Enter playlist link: ")
path = makeFolder(playlist_link, path)
print("Made Folder")

songs = getSongs(playlist_link)
print("Got Songs")

count = 0
failed = 0
total = len(songs)

for song in songs:

    print(song['track_name'])
    try:
        makeSong(song, path)
    except Exception as e:
        #print(e)
        failed += 1
    count += 1

    print(str(count) + ' / ' + str(total))
    
print("Failed: ", failed)