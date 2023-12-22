from django.urls import *
from django.shortcuts import * 
from django.contrib import messages

class ProfileSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if (
          request.user.is_authenticated 
          and not request.user.nickname # 먼저 유저가 로그인을 확인했는가?
          and request.path_info != reverse("profile-set") # 그리고 닉네임을 설정했는지?
          # 유저가 리퀘스트를 어디로 보냈는지?
          # 유저가 프로필 설정 페이지가 아닌 다른 페이지로 엉뚱한곳으로 갔는가? 확인 
        ):
            messages.warning(request,"프로필 설정이 필요합니다!") 
            return redirect("profile-set")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    # middleware 정의 