from django.shortcuts import render
from django.views.generic import * 
from django.db import models
from . models import * 
import datetime
import base64
from eightfortypy.models import * 
from datetime import datetime
import pymysql

# api 모듈 
from . use_api import * 
from . api_key import * 
# forms.py 
from eightfortypy.forms import * 
from django.urls import reverse,reverse_lazy
# Create your views here.

def index(request):
    return render(request,"main/index.html")


class MusicList(ListView):
    model = Song 
    template_name = 'main/list_page.html'
    context_object_name = "song"
    paginate_by = 20


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
def search_and_save_track(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        
        # 데이터베이스에서 음악 검색
        songs = Song.objects.filter(title__icontains=query)
        
        if not songs:
            # 데이터베이스에 음악이 없으면 Spotify API에서 검색 및 저장
            api = UseApi(client_id_spotify, client_pw_spotify)
            track_data = api.search_track(query)

            if track_data:
                
                # Artist 모델 생성
                artist_name = track_data["album"]["artists"][1]["name"]
                artist_id = track_data["album"]["artists"][0]["id"]
                artist, created = Artist.objects.get_or_create(
                    id=artist_id,
                    defaults={
                        "name": artist_name,
                    }
                )

                # Album 모델 생성
                album_id = track_data["album"]["id"]
                album, created = Album.objects.get_or_create(
                    id=album_id,
                    defaults={
                        "title": track_data["album"]["name"],
                        "release_date": datetime.strptime(track_data['album']['release_date'], '%Y-%m-%d'),
                        "artist": artist
                    }
                )

                # Song 모델 생성
                song_id = track_data['id']
                Song.objects.get_or_create(
                    id=song_id,
                    defaults={
                        "album": album,
                        "title": track_data['name'],
                        "popularity": track_data['popularity'],
                        "link": track_data['external_urls']['spotify']
                    }
                ),
                songs = Song.objects.filter(album=album)
    return render(request, 'main/search_result.html', {'songs': songs})
    