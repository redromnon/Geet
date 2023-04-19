from ytmusicapi import YTMusic
from pytube import YouTube
import os

tmpdir = None

def getaudio():

    path = os.path.join(os.getcwd(), tmpdir)

    if len(os.listdir(path)) != 0:
        for file in os.listdir(path):
            print("Found ", file)
            return os.path.join(tmpdir, file)
    
    else:
        print("No audio file found")
        return ""
        

def resetcache():

    #Delete audio dir
    path = os.path.join(os.getcwd(), tmpdir)
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
        print("File Deleted")


def searchsong(name):
    
    #Get search results
    result = YTMusic().search(query=name, filter="songs")

    #Create dict of songs with necessary keys
    songs_dict = {'songs':[]}

    for song in result:

        current_song_dict = {}

        current_song_dict.update({'name': song['title']})
        current_song_dict.update({'artists': song['artists'][0]['name']})
        current_song_dict.update({'videoId': song['videoId']})
        
        songs_dict['songs'].append(current_song_dict)

    return songs_dict


def dmusic(videoId):

    #Store videoid
    videourl = 'http://youtube.com/watch?v=' + str(videoId)
    yt = YouTube(videourl)

    #Filter stream
    stream = yt.streams.filter(only_audio=True, file_extension="mp4").last()
    
    #Download stream
    stream.download(output_path=f"{tmpdir}/")
    print("Music Downloaded")