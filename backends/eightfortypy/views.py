from django.shortcuts import render
from django.views.generic import * 
from django.db import models
from . models import * 
import datetime

from eightfortypy.models import * 
from datetime import datetime

# 페이지네이션
from django.core.paginator import Paginator
import requests

# api 모듈 
from . use_api import * 
from . api_key import * 
import base64

# forms.py 
from eightfortypy.forms import * 
from django.urls import reverse,reverse_lazy


def index(request):
    songs = Song.objects.all()  # 모든 Song 객체를 쿼리
    return render(request, "main/index.html", {'songs': songs})


class MusicList(ListView):
    model = Song 
    template_name = 'main/list_page.html'
    context_object_name = "song"
    paginate_by = 10


# 프로필 
class ProfileVeiw(DetailView):
    model = User 
    template_name = "main/profile.html"
    pk_url_kwarg = "user_id"
    
    context_object_name = "profile_user"
    
# 프로필 변경 

class ProfileUpdateView(UpdateView):
    model = User 
    form_class = ProfileForm 
    template_name = "main/profile_update_form.html"
    
    raise_exception = True # 접근자 제한 
    redirect_unauthenticated_users = False # 접근자 제한  
    
    def get_object(self,query=None):
        return self.request.user 
    
    def get_success_url(self):
        return reverse("profile",kwargs=({"user_id":self.request.user.id}))


#MySQL 서버에 연결
# connection = pymysql.connect(
#     host='localhost',
#     user='your_username',
#     password='your_password',
#     database='your_database_name'
# )

# 사용자 ID와 비밀번호로 MySQL에 인증하고 데이터베이스 선택
# cursor = connection.cursor()

# 예시: 데이터베이스에 데이터 추가
# sql = "INSERT INTO your_table_name (column1, column2, ...) VALUES (%s, %s, ...)"
# values = ('value1', 'value2', ...)
# cursor.execute(sql, values)

# # 변경사항 저장
# connection.commit()

# # 연결 닫기
# cursor.close()
# connection.close()

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
        related_artists = self.get_related_artists(artist_data['id'])
        top_tracks = self.get_top_tracks(artist_data['id'])
        self.track_data['related_artists'] = related_artists
        self.track_data['top_tracks'] = top_tracks
        each_track = []
        related_track = []
        for track in top_tracks:
            track_id = track["id"]
            album_id = track["album"]["id"]
            album_name = track["album"]["name"]
            name = track["name"]
            artist_name = track["artists"][0]["name"]
            image = track["album"]["images"][0]["url"]
            popularity = track["popularity"]
            link = track["external_urls"]
            each_track.append(dict(track_id = track_id, album_id = album_id, album_name = album_name, track_name = name, artist_name = artist_name, popularity = popularity, image = image, link = link))
        for track in related_artists:
            artist_id = track["id"]
            artist_name = track["name"]
            genres = ", ".join(track["genres"])
            image = track["images"][0]["url"]
            popularity = track["popularity"]
            link = track["external_urls"]
            related_track.append(dict(artist_id = artist_id, artist_name = artist_name, genres = genres, popularity = popularity, image = image, link = link))
            
        self.track_data['artist_info'] = artist_data  # Adding artist info to track_data
        self.album_data = dict(album_id = self.track_data["album"]["id"], album_name = self.track_data["album"]["name"], release_data = self.track_data["album"]["release_date"], album_image = self.track_data["album"]["images"][0]["url"], album_link = self.track_data["album"]["external_urls"])
        self.artist_data = dict(artist_id = self.track_data["artist_info"]["id"], artist_name = self.track_data["artist_info"]["name"], artist_popularity = self.track_data["artist_info"]["popularity"], artist_genres = ",".join(self.track_data["artist_info"]["genres"]), artist_image = self.track_data["artist_info"]["images"][0]["url"], artist_link = self.track_data["artist_info"]["external_urls"])
        self.song_data = dict(track_id = self.track_data["id"], track_name = self.track_data["name"], track_popularity = self.track_data["popularity"], track_image = self.track_data["album"]["images"][0]["url"], track_link= self.track_data["external_urls"])
        return self.album_data, self.artist_data, self.song_data, each_track, related_track
    
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
    
    def get_related_artists(self, artist_id):
        related_artists_endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
        related_artists_response = requests.get(related_artists_endpoint, headers=self.headers)
        related_artists_data = related_artists_response.json()
        return related_artists_data['artists'] if 'artists' in related_artists_data else []

    def get_top_tracks(self, artist_id):
        top_tracks_endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'  # Example using US market
        top_tracks_response = requests.get(top_tracks_endpoint, headers=self.headers)
        top_tracks_data = top_tracks_response.json()
        return top_tracks_data['tracks'] if 'tracks' in top_tracks_data else []
# 음악 검색 
def search_track(request):
    context = {}
    if request.method == "POST":
        track_name = request.POST.get('query')
        api = UseApi(client_id_spotify,client_pw_spotify)  # Spotify API 인스턴스 생성
        album_data, artist_data, song_data = api.search_track(track_name)

        # 아티스트 정보 확인 및 저장
        artist, created = Artist.objects.get_or_create(id=artist_data['artist_id'], defaults={
            'name': artist_data['artist_name'],
            'image': artist_data['artist_image'],
            'genres': artist_data['artist_genres'],
            'popularity': artist_data['artist_popularity']
        })

        # 앨범 정보 확인 및 저장
        album, created = Album.objects.get_or_create(id=album_data['album_id'], defaults={
            'title': album_data['album_name'],
            'artist': artist,
            'release_date': album_data['release_data'],
            'image': album_data['album_image']
        })

        # 곡 정보 확인 및 저장
        song, created = Song.objects.get_or_create(id=song_data['track_id'], defaults={
            'title': song_data['track_name'],
            'album': album,
            'popularity': song_data['track_popularity'],
            'link': song_data['track_link']['spotify']
        })

        album_songs = Song.objects.filter(album=album).order_by('title')
        
        paginator = Paginator(album_songs, 10)  # 여기서 10은 한 페이지에 표시할 항목 수
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # 검색 결과를 context에 추가
        context = {
            'artist': artist,
            'album': album,
            'song': song,
            'album_songs': album_songs,
            'created': created
        }

    # 검색 결과와 함께 템플릿 렌더링
    return render(request, 'main/search_result.html', context)
    