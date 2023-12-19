from django.shortcuts import render
from django.views.generic import * 
from django.db import models
from models import * 
import datetime
import base64
from eightfortypy.models import * 
# Create your views here.

def index(request):
    return render(request,"main/index.html")

class UseApi:
    def __init__(self, cli_id, cli_sec):
        client_id = cli_id
        client_secret = cli_sec
        token_endpoint = 'https://accounts.spotify.com/api/token'
        payload = {'grant_type': 'client_credentials'}
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        }
        token_response = requests.post(token_endpoint, data=payload, headers=headers)
        token_data = token_response.json()
        access_token = token_data['access_token']
        # Fetch data from Spotify API using search query
        self.headers = {'Authorization': 'Bearer ' + access_token}
        print("Authorization complete")
        
    def search_track(self, track_name):
        search_endpoint = f'https://api.spotify.com/v1/search?q={track_name}&type=track'
        search_response = requests.get(search_endpoint, headers=self.headers)
        search_data = search_response.json()
        track_id = search_data['tracks']['items'][0]['id']  # Get track ID from the first search result
        
        track_endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        track_response = requests.get(track_endpoint, headers=self.headers)
        self.track_data = track_response.json()
        artist_name = self.track_data['artists'][0]['name']
        artist_data = self.search_artist(artist_name)
        
        self.track_data['artist_info'] = artist_data  # Adding artist info to track_data
        self.album_data = dict(album_id = self.track_data["album"]["id"], album_name = self.track_data["album"]["name"], release_data = self.track_data["album"]["release_date"], album_image = self.track_data["album"]["images"][0]["url"], album_link = self.track_data["album"]["external_urls"])
        self.artist_data = dict(artist_id = self.track_data["artist_info"]["id"], artist_name = self.track_data["artist_info"]["name"], artist_popularity = self.track_data["artist_info"]["popularity"], artist_genres = ",".join(self.track_data["artist_info"]), artist_image = self.track_data["artist_info"]["images"][0]["url"], artist_link = self.track_data["artist_info"]["external_urls"])
        self.song_data = dict(track_id = self.track_data["id"], track_name = self.track_data["name"], track_popularity = self.track_data["popularity"], track_image = self.track_data["album"]["images"][0]["url"], track_link= self.track_data["external_urls"])
        return self.album_data, self.artist_data, self.song_data

    def search_artist(self, artist_name):
        search_endpoint = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist'
        search_response = requests.get(search_endpoint, headers=self.headers)
        search_data = search_response.json()
        artist_id = search_data['artists']['items'][0]['id']  # Get artist ID from the first search result
        # Fetch artist data from Spotify API using artist ID
        artist_endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'
        artist_response = requests.get(artist_endpoint, headers=self.headers)
        self.artist_data = artist_response.json()
        return self.artist_data