from django.shortcuts import redirect
from allauth.account.utils import send_email_confirmation


def confirmation_required_redirect(self,request):
    send_email_confirmation(request,request.user) # 유저에게 인증 이메일을 발송시킴 
    return redirect("account_email_confirmation_required") # 인증이 필요한 페이지로 리다이렉트