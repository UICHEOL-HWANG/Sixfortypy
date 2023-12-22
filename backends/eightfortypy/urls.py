from django.urls import path
from . import views
from .models import * 

urlpatterns = [
    path('',views.index,name="index"),
    
    #음악 목록 
    path('music_list/',views.MusicList.as_view(),name="music-list"),
    # 추천
    path('music_recommended/<int:user_id>/', views.RecommendedView.as_view(), name="recommend"),

    
    
    
    ## 디테일 페이지 
    # 음악 디테일 
    path('music/<str:song_id>/',views.MusicDetailView.as_view(), name='music_detail'),
    # 앨범 디테일 
    path('album/<str:album_id>/',views.AlbumDetailView.as_view(), name='album_detail'),
    # 아티스트 디테일 
    path('artist/<str:artist_id>/',views.ArtistDetailView.as_view(), name='artist_detail'),
    
    ## 계정관련
    # 프로필 
    path('users/<int:user_id>/',views.ProfileView.as_view(),name = "profile"),   
    # 프로필 수정 
    path('edit-profile/',views.ProfileUpdateView.as_view(),name="profile-update"),
    # 검색결과 
    path('search/', views.search_track, name='search_and_save_track'),
    # 프로필 북마크 
    path('bookmark/song/',views.BookmarkSongView.as_view(), name='bookmark_song'),
    
    
]
