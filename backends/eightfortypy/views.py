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

# 추천시스템을 위한 모듈 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def index(request):
    songs = Song.objects.all()  # 모든 Song 객체를 쿼리
    return render(request, "main/index.html", {'songs': songs})


class MusicList(ListView):
    model = Song
    template_name = 'main/list_page.html'
    context_object_name = "songs"  # 이것을 복수형으로 변경하는 것이 좋습니다.
    paginate_by = 10

    def get_queryset(self):
        # Album과 관련된 Song 객체를 가져오기
        return Song.objects.select_related('album').all()


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


# 특정 음악 클릭했을 때 디테일 페이지
# Song,Album,Artists 모두 연결 
class MusicDetailView(DetailView):
    model = Song
    template_name = "main/detail_page.html"
    pk_url_kwarg = 'song_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object  # 현재 곡 객체
        context['album'] = song.album  # 연결된 앨범
        context['artist'] = song.album.artist  # 연결된 아티스트
        
        # 해당 곡과 관련한 앨범 내 곡들을 더 추가하기 위한 로직 
        artist_id = song.album.artist.id
        context['other_songs'] = Song.objects.filter(album__artist__id=artist_id).exclude(id=song.id)
        return context

# 앨범 디테일 페이지 

class AlbumDetailView(DetailView):
    model = Album
    template_name = "main/album_detail_page.html"
    pk_url_kwarg = 'album_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.object  # 현재 앨범 객체
        context['songs'] = Song.objects.filter(album=album)  # 현재 앨범과 연결된 곡들
        context['artist'] = album.artist  # 현재 앨범과 연결된 아티스트
        
        # 코사인 유사도 
        
        # 모든 아티스트의 장르 데이터 가져오기
        all_artists = Artist.objects.all()
        genres = [artist.genres for artist in all_artists]  # 예시: 각 아티스트의 장르 사용

        # TF-IDF 벡터화
        vectorizer = TfidfVectorizer()
        genre_matrix = vectorizer.fit_transform(genres)

        # 현재 아티스트와 다른 아티스트들 간의 코사인 유사도 계산
        cosine_similarities = cosine_similarity(genre_matrix, genre_matrix)
        current_artist_index = list(all_artists).index(album.artist)
        similarity_scores = list(enumerate(cosine_similarities[current_artist_index]))

        # 유사도에 따라 아티스트 정렬 및 상위 N개 추출
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommended_artist_ids = [all_artists[i].id for i, score in similarity_scores[1:6]]  # 상위 5개, 현재 아티스트 제외

        # 추천 아티스트
        context['recommended_artists'] = Artist.objects.filter(id__in=recommended_artist_ids)

        return context

class ArtistDetailView(DetailView):
    model = Artist
    template_name = "main/artist_detail_page.html"
    pk_url_kwarg = "artist_id"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist_id = self.kwargs.get('artist_id')
        # Song 모델에서 아티스트를 찾을 때 album을 통해 접근
        context['songs'] = Song.objects.filter(album__artist__id=artist_id)
        
        # 고유한 앨범 목록 추가
        unique_albums = Album.objects.filter(artist__id=artist_id).distinct()
        context['unique_albums'] = unique_albums

        return context

    
# 음악 검색 
def search_track(request):
    context = {}
    if request.method == "POST":
        track_name = request.POST.get('query')
        api = UseApi(client_id_spotify, client_pw_spotify)  # Spotify API 인스턴스 생성
        album_data, artist_data, song_data, each_track, related_track = api.search_track(track_name)

        # 아티스트 정보 확인 및 저장
        artist, created = Artist.objects.get_or_create(id=artist_data['artist_id'], defaults={
            'name': artist_data['artist_name'],
            'image': artist_data['artist_image'],
            'genres': artist_data['genres'],
            'popularity': artist_data['artist_popularity']
        })

        # 앨범 정보 확인 및 저장
        album, created = Album.objects.get_or_create(id=album_data['album_id'], defaults={
            'title': album_data['album_name'],
            'artist': artist,
            'release_date': album_data['release_date'],
            'image': album_data['album_image']
        })

        # 곡 정보 확인 및 저장
        song, created = Song.objects.get_or_create(id=song_data['track_id'], defaults={
            'title': song_data['track_name'],
            'album': album,
            'popularity': song_data['track_popularity'],
            'link': song_data['track_link'][0]
        })

        # 각 트랙 정보 처리
        for track in each_track:
            track_artist, _ = Artist.objects.get_or_create(id=track['artist_id'], defaults={
                'name': track['artist_name'],
                'popularity': track['popularity']
            })

            track_album, _ = Album.objects.get_or_create(id=track['album_id'], defaults={
                'title': track['album_name'],
                'artist': track_artist,
                'image': track['image'],
                'release_date': track['release_date']
            })

            Song.objects.get_or_create(id=track['track_id'], defaults={
                'title': track['track_name'],
                'album': track_album,
                'popularity': track['popularity'],
                'link': track['link']
            })

        # 관련 아티스트 정보 처리
        related_artists = []  # 빈 리스트로 초기화
        for related in related_track:
            related_artist, _ = Artist.objects.get_or_create(id=related['artist_id'], defaults={
                'name': related['artist_name'],
                'image': related['image'],
                'popularity': related['popularity'],
                'genres': related['genres']
            })
            related_artists.append(related_artist)  # 관련 아티스트 목록에 추가

        album_songs = Song.objects.filter(album=album).order_by('title')
        
        paginator = Paginator(album_songs, 10)  # 여기서 10은 한 페이지에 표시할 항목 수
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # 검색 결과를 context에 추가
        context = {
            'artist': artist,
            'album': album,
            'song': song,
            'album_songs': page_obj,
            'each_track': each_track,  # 각 곡의 데이터
            'related_artists': related_artists,  # 관련 아티스트의 데이터
        }

    # 검색 결과와 함께 템플릿 렌더링
    return render(request, 'main/search_result.html', context)
