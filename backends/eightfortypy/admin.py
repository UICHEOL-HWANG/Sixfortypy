from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import * 
from django.contrib.auth.admin import UserAdmin


admin.site.register(User,UserAdmin)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 관리자 페이지에서 표시할 필드
    search_fields = ('name',)  # 검색 기능에 사용할 필드

# Album 모델을 위한 Admin 클래스
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    list_filter = ('artist', 'release_date')  # 필터 옵션
    search_fields = ('title', 'artist__name')  # 앨범 이름 및 아티스트 이름으로 검색

# Song 모델을 위한 Admin 클래스
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'popularity')
    list_filter = ('album__artist', 'album')  # 앨범 아티스트 및 앨범으로 필터
    search_fields = ('title', 'album__title', 'album__artist__name')  # 곡 이름, 앨범 이름, 아티스트 이름으로 검색

# 모델들을 admin 사이트에 등록
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
>>>>>>> d717f5d4ffb90cfb12c5bd52259361ce19ef6e18
