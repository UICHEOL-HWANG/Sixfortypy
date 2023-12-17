from django import forms 
from .models import *
from eightfortypy.models import * 

        
# 프로필 수정 폼 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = [
            "nickname",
            "profile_pic",
            "intro" # 소개글이 들어가는데 디폴트 데이터값이 textinput이 들어간다 근데 용량이 매우 적음 
        ]
        widgets = {
            # 프로필 바꾸기 양식 
            "profile_pic": forms.FileInput,
            "intro" : forms.Textarea # textarea로 데이터 크기를 맞춰줌 
            }
            