from django.urls import path
from . import views
from .models import * 

urlpatterns = [
    path('',views.index,name="index"),
<<<<<<< HEAD
=======
    path('music_list/',views.MusicList.as_view(),name="music-list")
>>>>>>> d717f5d4ffb90cfb12c5bd52259361ce19ef6e18
]
