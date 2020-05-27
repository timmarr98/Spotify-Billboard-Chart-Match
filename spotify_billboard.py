import sys
import spotipy
import json
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import billboard
from datetime import date

SPOTIPY_CLIENT_ID = '690ca0d6123d44d58bafca609139ef3d'
SPOTIPY_CLIENT_SECRET = '70f9a6dbedae4c13b3b0756131ac7db0'
SPOTIPY_REDIRECT_URI = 'http://www.google.com/'

chart = billboard.ChartData('hot-100') #get the top 100 chart from Billboard API

scope = 'user-library-read'
username = 'junketsu98'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) 

token = util.prompt_for_user_token(username, scope, client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = 'http://www.google.com/')

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
    sp = spotipy.Spotify(auth=token)
    timmy = sp.current_user()
    topSong = spotify.playlist_tracks('spotify:playlist:37i9dQZEVXbLRQDuF5jeBp')  # get URI for spotify playlist
    # artist = topSong['items'][0]['track']['album']['artists'][0]
    # print(artist['name'])

    print("Artists in playlist")
    print("---------------------")

    artists = set() #implement a set to guarantee that there are no duplicate artists 

    for item in topSong['items']: #items is the outter JSON 
        artist = item['track']['album']['artists'][0] #going down to find the artist name
        print( "---------", artist['name'], "---------")
        artists.add(str(artist['name'])) #add the artists to the 
    for item in artists:
        billboardSearch(item)

else:
    print("Can't get token for", username)
