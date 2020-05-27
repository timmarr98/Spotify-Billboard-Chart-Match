api_key = "AIzaSyBb8OGJMpiTG74IcmuLaPJdCSMONBgEpg0"
from googleapiclient.discovery import build
import json
import pprint
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl

youtube = build('youtube', 'v3',developerKey = api_key)

req = youtube.playlistItems().list( # pylint: disable=no-member
    part="snippet",
    playlistId="PLxhnpe8pN3TmtjcQM7zcYAKhQXPdOHS3Y",
    maxResults=20)

res = req.execute()
scope = 'playlist-modify-public'
username = 'junketsu98'

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

if token:
    sp = spotipy.Spotify(auth = token)
    playlist = sp.user_playlist_create(username, "TEST HOE!")
    playlist__ID = playlist['id']
    print(playlist__ID)


def getArtist_Song(x):
    Songs = set()
    for item in x['items']:
        #print(json.dumps(item, indent =4))
        videoURI = "https://www.youtube.com/watch?v={}".format(item['snippet']['resourceId']['videoId'])
 
       #To obtain the official song title and artist from the youtube_dl database
        video = youtube_dl.YoutubeDL({}).extract_info(videoURI, download = False)
   
        
        artiste = video["artist"]
        song_name = video["track"]
        if (artiste != "None" or song_name != "None") :
         artiste = video["artist"]
         song_name = video["track"]
        if(artiste is None):
         print("The YouTube database does not have an official Artist name!")
         continue
        if(video is None):
         print("The YouTube database does not have an official Video name!")
         continue
  
        #print(artiste, song_name)
    
        #search the girls
        results = sp.search(q = (artiste+ " " +song_name), limit =1 )

        try:
            song_id = str(results['tracks']['items'][0]['id'])
        except IndexError:
            artiste is None or video is None
        if (artiste is not None and video is not None):
         Songs.add("spotify:track:" + song_id)
        #print(song_id)
        #add to a playlist
       # sp.user_playlist_add_tracks(username, playlist__ID,"spotify:track:{song_id} )
    sp.user_playlist_add_tracks(username, playlist__ID, Songs )

getArtist_Song(res)
   
