from pytubefix import Search
import os
import eyed3
from moviepy.editor import *
import urllib.request 
import shutil

def getAudio(song):
    s = Search(song["track_name"] + " " + song["artists"] + " audio")

    streams = []
    worst_quality = 0
    for result in s.results:
        if song["track_length"] - 3 <= result.length <= song["track_length"] + 3:
            curr = result.streams.filter(only_audio=True).order_by('abr')
            curr = list(curr)[::-1]
            streams += [curr]
            worst_quality = max(worst_quality, len(curr))

    quality_index = 0

    while quality_index < worst_quality:
        for i in range(len(streams)):
            if quality_index >= len(streams[i]):
                continue

            stream = streams[i][quality_index]
            if stream != None:
                try:
                    file = stream.download(output_path="./Temp")
                    if(file == None):
                        continue
                    else:
                        return file
                except Exception as e:
                    #print(e)
                    continue


def getArtwork(link):
    urllib.request.urlretrieve(link, "./Temp/img.jpg")

def to_mp3(file, mp3):
    audio = AudioFileClip(file)
    audio.write_audiofile(mp3, logger = None)
    audio.close()


def makeSong(song, path):
    file_name = song["artists"] + ' - ' + song["track_name"]
    bad_chars = [':', '!', "*", "/", "\\", "?", "|", "<", ">", '"']
    for i in bad_chars:
        file_name = file_name.replace(i, '')
    
    new_file = path + '/' + file_name +'.mp3'
    if os.path.exists(new_file): 
        print("already exists")
        return
    
    file = getAudio(song)
    if file == None:
        print("Not found")
        return

    to_mp3(file, new_file)

    getArtwork(song["img_url"])
    img = open('./Temp/img.jpg', 'rb')

    f = eyed3.load(new_file)
    f.tag.artist = song["artists"]
    f.tag.title = song["track_name"]
    f.tag.album = song["album_name"]
    f.tag.images.set(3, img.read(), 'image/jpeg')
    f.tag.save(version=eyed3.id3.ID3_V2_3)

    f.tag.save()
    img.close()

    shutil.rmtree('./Temp')
