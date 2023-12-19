<<<<<<< HEAD
"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('eightfortypy.urls')),
]
=======
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
>>>>>>> d717f5d4ffb90cfb12c5bd52259361ce19ef6e18
