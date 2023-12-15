from django.urls import path
from . import views
from .models import * 

urlpatterns = [
    path('',views.index,name="index"),
    path('music_list/',views.MusicList.as_view(),name="music-list")
]
