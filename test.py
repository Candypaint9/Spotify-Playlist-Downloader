from pytubefix import YouTube
from pytubefix import Search
import os
import eyed3
from moviepy.editor import *
import urllib.request 
import shutil

def getmp4(track_name, artist_name):
    s = Search(track_name + " " + artist_name + " audio only lyrics")

    destination = "./Temp"

    for result in s.results:
        streams = result.streams
        for stream in streams.all():
            if stream != None:
                file = stream.download(output_path=destination)

                return file


def getArtwork(link):
    
    urllib.request.urlretrieve(link, "./Temp/img.jpg")

def mp4_to_mp3(mp4, mp3):
    video = VideoFileClip(mp4)
    audio = video.audio
    audio.write_audiofile(mp3, logger = None)
    video.close()
    audio.close()


def makeSong(song, playlist_name):
    
    artist_name = song["artist_name"]
    track_name = song["track_name"]
    album_name = song["album_name"]
    file = getmp4(track_name, artist_name)

    #print(file)

    if file == None:
        return

    #convert to mp3
    name = artist_name + ' - ' + track_name
    bad_chars = [':', '!', "*", "/", "\\", "?", "|", "<", ">", '"']

    for i in bad_chars:
        name = name.replace(i, '')
    
    new_file = './' + playlist_name + '/' + name +'.mp3'
    mp4_to_mp3(file, new_file)



    getArtwork(song["img_url"])
    img = open('./Temp/img.jpg', 'rb')

    f = eyed3.load(new_file)
    f.tag.artist = artist_name
    f.tag.title = track_name
    f.tag.album = album_name
    f.tag.images.set(3, img.read(), 'image/jpeg')
    f.tag.save(version=eyed3.id3.ID3_V2_3)

    f.tag.save()

    img.close()


    shutil.rmtree('./Temp')

#makeSong({"artist_name":'Meduza', "track_name":'Bad Memories (feat Elley Duh FAST BOY)', "album_name":'ez', "img_url":"https://i.pinimg.com/736x/63/a0/08/63a008f631ae7492a75a001bd0791e8f.jpg"}, 'Test')
#getmp3()
#mp4_to_mp3('./Temp\Miki Matsubara- Mayonaka No Door (Stay With Me) Lyrics.mp4', './Liked/Miki Matsubara- Mayonaka No Door (Stay With Me).mp3')
