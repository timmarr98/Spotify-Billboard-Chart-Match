api_key = input("Enter your youtube API key: ")
from googleapiclient.discovery import build
import json
import pprint
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl

#initialize the youtube API 
youtube = build('youtube', 'v3',developerKey = api_key)

#get the request for playlist videos 
req = youtube.playlistItems().list( # pylint: disable=no-member
    part="snippet",
    playlistId="PLxhnpe8pN3TmtjcQM7zcYAKhQXPdOHS3Y",
    maxResults=20)

#execute the request 
res = req.execute()

scope = 'playlist-modify-public'
username = input("Enter your Spotify Username: ")

#pass user name and scope to token 
token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#if the token is valid, continue 
if token:
    sp = spotipy.Spotify(auth = token)
    playlist = sp.user_playlist_create(username, "Generated Playlist")
    playlist__ID = playlist['id']
    print(playlist__ID)

#get the artist and song from 
def getArtist_Song(x):
    Songs = set() #Set of non-duplicate artists/songs
    for item in x['items']: #iterate through the items in the playlist
      
        #format the URL 
        videoURI = "https://www.youtube.com/watch?v={}".format(item['snippet']['resourceId']['videoId'])
 
       #To obtain the official song title and artist from the youtube_dl database
        video = youtube_dl.YoutubeDL({}).extract_info(videoURI, download = False)
   
        
        artiste = video["artist"]
        song_name = video["track"]
        if(artiste is None):
         print("The YouTube database does not have an official Artist name!")
         continue
        if(video is None):
         print("The YouTube database does not have an official Video name!")
         continue
    
        #Search Spotify for the songs
        results = sp.search(q = (artiste+ " " +song_name), limit =1 )

        try:
            song_id = str(results['tracks']['items'][0]['id'])
        except IndexError:
            artiste is None or video is None
        if (artiste is not None and video is not None):
         Songs.add("spotify:track:" + song_id)
    sp.user_playlist_add_tracks(username, playlist__ID, Songs )

getArtist_Song(res)
   
