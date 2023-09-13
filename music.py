from ytmusicapi import YTMusic
from pytube import YouTube
import os

def createcache():

    try:
        os.makedirs("cache")
        print("Created cache")
    except FileExistsError:
        print("cache present")


def getaudio():

    path = os.path.join(os.getcwd(), "cache")

    if len(os.listdir(path)) != 0:
        for file in os.listdir(path):
            print("Found ", file)
            return file

    else:
        print("No audio file found")
        return "fake.mp4"
        

def resetcache():

    #Delete audio dir
    path = os.path.join(os.getcwd(),"cache")
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
        current_song_dict.update({'duration': song['duration']})
        current_song_dict.update({'isExplicit': "(Explicit) - " if song['isExplicit'] else ""})


        songs_dict['songs'].append(current_song_dict)

    return songs_dict


def dmusic(videoId):

    #Store videoid
    videourl = 'http://youtube.com/watch?v=' + str(videoId)
    yt = YouTube(videourl)

    #Filter stream
    stream = yt.streams.filter(only_audio=True, file_extension="webm").first()
    
    #Download stream
    stream.download(output_path="cache/")
    print("Music Downloaded")