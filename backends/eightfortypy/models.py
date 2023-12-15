from django.db import models
from django.contrib.auth.models import AbstractUser # 회원가입 모델 
from django.contrib.auth.models import User

class User(AbstractUser):
    nickname = models.CharField(max_length=15,unique=True,null=True,
                                error_messages={'unique':'이미 사용중인 닉네임'},
                                ) # 최대 길이 15자, 유일성 유지 
    
    profile_pic = models.ImageField(default="default_profile_pic.jpg",
                                    upload_to="profile_pics",
                                    blank=True) # 프로필 사진 안 올리면 기본 사진으로

    intro = models.CharField(max_length=60,blank=True) # 자기소개
    
    def __str__(self):
        return self.email 

class Profile(models.Model):
    intro = models.CharField(max_length=60, blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nickname
    

class Music(models.Model):
    Album = models.CharField(max_length=30)
    Title = models.CharField(max_length=30)
    Genre = models.CharField(max_length=30)
    Release_Date = models.DateField()
    Album_Image = models.ImageField(upload_to='Album_pics',blank=True)