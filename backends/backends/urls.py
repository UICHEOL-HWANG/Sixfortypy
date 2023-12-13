from django.contrib import admin
from django.urls import path,include

# 이메일 인증 관련 
from django.views.generic import TemplateView 
# 제네릭 뷰에 있는 템플릿 뷰를 사용하므로서 따로 view를 만들어주지 않아도 됨 

from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # main-site
    path('',include('eightfortypy.urls')),
    
    # 이메일 인증 완료 
    path('accounts/',include('allauth.urls')),
    
    # 이메일 인증
    path('email-confirmation-required/',
    TemplateView.as_view(template_name="account/email_confirmation_required.html")
    ,name="account_email_confirmation_required"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)