from braces.views import LoginRequiredMixin,UserPassesTestMixin
from allauth.account.models import EmailAddress
from .functions import confirmation_required_redirect

class LoginAndVerificationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    redirect_unauthenticated_users = True # 로그인이 안되어 있는 유저는 로그인 
    raise_exception = confirmation_required_redirect # 로그인은 했지만 인증이 안된 애들은 
    
        
    # 사용자 접근 제한 
    def test_func(self, user): # User가 게시물에 접근할 수 있는지 없는지를 boolean 값으로 리턴 해줌 
        return EmailAddress.objects.filter(user=user,verified=True).exists()
            # 현재 사용자가 등록이 되어 있고 / 이메일 인증을 했는지 2가지를 확인하는 절차 
            # admin에 이메일이라는 섹션이 생김 
            

    

class LoginAndOwnershipRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):    
    raise_exception = True #
    redirect_unauthenticated_users = False # 
    
    def test_func(self,user_id):
        user_id = self.kwargs.get('user_id')
        return self.request.user.id == int(user_id)