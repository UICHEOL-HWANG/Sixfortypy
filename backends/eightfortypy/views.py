from django.shortcuts import render
from django.views.generic import * 
from django.db import models
from . models import * 
import datetime

from eightfortypy.models import * 
from datetime import datetime

# 페이지네이션
from django.core.paginator import Paginator

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
    