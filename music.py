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
            return os.path.join("cache", file)
    
    else:
        print("No audio file found")
        return ""

def resetcache():

    #Delete audio dir
    path = os.path.join(os.getcwd(),"cache")
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
        print("File Deleted")


def searchsong(name):
    result = YTMusic().search(query=name, filter="songs")

    return result


def dmusic(videoId):

    #Store videoid
    videourl = 'http://youtube.com/watch?v=' + str(videoId)
    yt = YouTube(videourl)

    #Filter stream
    stream = yt.streams.filter(only_audio=True, file_extension="mp4").last()
    
    #Download stream
    stream.download(output_path="cache/")
    print("Music Downloaded")