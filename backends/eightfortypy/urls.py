from django.urls import path
from . import views
from .models import * 

urlpatterns = [
    path('',views.index,name="index"),
    path('music_list/',views.MusicList.as_view(),name="music-list"),
    
    # 프로필 
    path('users/<int:user_id>/',views.ProfileVeiw.as_view(),name = "profile"),
        
    # 프로필 수정 
    path('edit-profile/',views.ProfileUpdateView.as_view(),name="profile-update"),
    
]
