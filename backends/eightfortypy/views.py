from django.shortcuts import render
from models import *
import pymysql
import base64
import requests
import datetime
# Create your views here.

def index(request):
    return render(request,"main/index.html")

connection = pymysql.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database_name'
)

# # 사용자 ID와 비밀번호로 MySQL에 인증하고 데이터베이스 선택
# cursor = connection.cursor()

# # 예시: 데이터베이스에 데이터 추가
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
        
        self.track_data['artist_info'] = artist_data  # Adding artist info to track_data
        self.album_data = dict(album_id = self.track_data["album"]["id"], album_name = self.track_data["album"]["name"], release_data = self.track_data["album"]["release_date"], album_image = self.track_data["album"]["images"][0]["url"], album_link = self.track_data["album"]["external_urls"])
        self.artist_data = dict(artist_id = self.track_data["artist_info"]["id"], artist_name = self.track_data["artist_info"]["name"], artist_popularity = self.track_data["artist_info"]["popularity"], artist_genres = ",".join(self.track_data["artist_info"]), artist_image = self.track_data["artist_info"]["images"][0]["url"], artist_link = self.track_data["artist_info"]["external_urls"])
        self.song_data = dict(track_id = self.track_data["id"], track_name = self.track_data["name"], track_popularity = self.track_data["popularity"], track_image = self.track_data["album"]["images"][0]["url"], track_link= self.track_data["external_urls"])
        return self.album_data, self.artist_data, self.song_data
    
    # def to_database(self, mysql_connection_info):
    #     connection = pymysql.connect(**mysql_connection_info)
    #     cursor = connection.cursor()
    #     if not self.track_data:
    #         return

    #     track_info = self.track_data

    #     # Music 모델에 데이터 삽입
    #     try:
    #         Music.objects.create(
    #             Album=track_info['album']['name'],
    #             Title=track_info['name'],
    #             Genre=', '.join(track_info['artists'][0]['genres']),  # 리스트 형태의 장르를 문자열로 변환
    #             Release_Date=datetime.strptime(track_info['album']['release_date'], '%Y-%m'),  # 날짜 형식 변환 필요
    #             Album_Image=track_info["album"]["images"][0]["url"],
    #             Artist = track_info["album"]["artists"][0]["name"],
    #             Popularity = track_info["popularity"],
    #             Artist_Image = track_info,
    #             Artist_Id = track_info["artists"][0]["id"],
    #             Track_Id = track_info["id"],
    #             Link = track_info["external_urls"]["spotify"]
    #         )
    #     except Exception as e:
    #         print(f"Failed to insert data: {e}")
    #     cursor.close()
    #     connection.close()