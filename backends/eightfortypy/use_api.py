import requests
import json 
import base64

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
        
        # Fetch track data from Spotify API using track ID
        track_endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        track_response = requests.get(track_endpoint, headers=self.headers)
        self.track_data = track_response.json()
        
        # Fetch audio features for the track using track ID
        audio_features_endpoint = f'https://api.spotify.com/v1/audio-features/{track_id}'
        audio_features_response = requests.get(audio_features_endpoint, headers=self.headers)
        audio_features_data = audio_features_response.json()
        
        # Combine track_data and audio_features_data
        self.track_data['audio_features'] = audio_features_data  # Adding audio features to track_data
        
        return self.track_data
    
    
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