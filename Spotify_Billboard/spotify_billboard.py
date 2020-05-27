import sys
import spotipy
import json
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import billboard
from datetime import date

#Spotify variables to use the Spotify/Spotipy(python version) web API
SPOTIPY_CLIENT_ID = input("Enter your Spotify ID: ")
SPOTIPY_CLIENT_SECRET = input("Enter your Secret Spotify ID: ")
SPOTIPY_REDIRECT_URI = input("Enter your Redirect URI: ")

#get the top 100 chart from Billboard API
chart = billboard.ChartData('hot-100')

scope = 'user-library-read'
username = input("Enter your Spotify Username:")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) 

#Set some variables for the environment and pass themt through the user token function
token = util.prompt_for_user_token(username, scope, client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI)

#Search for the artist on billboard
def billboardSearch(personArtist):
    print("These are artist %s's current top 100 entries" % (personArtist))
    count = 0
    for i in chart:
        if personArtist in str(i.artist):
            count += 1
            print('#',i.rank, i.title, "at", i.weeks, "weeks on the charts")
    print("------ %d entries as of today ------- "% (count))
    print("")


if token: 
    topSong = spotify.playlist_tracks('spotify:playlist:37i9dQZEVXbLRQDuF5jeBp')  # get URI for spotify playlist

    print("Artists in playlist")
    print("---------------------")

    #implement a set to guarantee that there are no duplicate artists
    artists = set()  

    for item in topSong['items']: #items is the outter JSON 
        artist = item['track']['album']['artists'][0] #going down to find the artist name
        print( "---------", artist['name'], "---------")
        artists.add(str(artist['name'])) #add the artists to the 
    for item in artists:
        billboardSearch(item) #search the "artist" in the set on billboard

else:
    print("Can't get token for", username)
