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

    