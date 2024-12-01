from pytubefix import Search
import os
import eyed3
from moviepy.editor import *
import urllib.request 
import shutil

def getAudio(song):
    s = Search(song["track_name"] + " " + song["artists"] + " audio only lyrics")

    streams = []

    for result in s.results:
        if song["track_length"] - 3 <= result.length <= song["track_length"] + 3:
            curr = result.streams.filter(only_audio=True).order_by('abr')
            streams.extend(curr[:min(3, len(curr))])

    for stream in streams:
        if stream != None:
            try:
                file = stream.download(output_path="./Temp")
                if(file == None):
                    continue
                else:
                    return file
            except Exception as e:
                print(e)
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

#makeSong({"artists":'Meduza', "track_name":'Bad Memories (feat Elley Duh FAST BOY)', "album_name":'ez', "img_url":"https://i.pinimg.com/736x/63/a0/08/63a008f631ae7492a75a001bd0791e8f.jpg", "track_length":149}, 'Test')
#getmp3()
#mp4_to_mp3('./Temp\Miki Matsubara- Mayonaka No Door (Stay With Me) Lyrics.mp4', './Liked/Miki Matsubara- Mayonaka No Door (Stay With Me).mp3')
