"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import include, path,re_path
from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.conf import settings
from backend.settings import MEDIA_ROOT, MEDIA_URL
from jfootball_record.views.sign_up_view import SignupView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
@login_required
def index_view(request,*args, **kwargs):
    return render(request, 'index.html')

urlpatterns = [
    path('sign_up/', SignupView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/v1/', include('jfootball_record.urls')),
    re_path(r'^my_app/(?!.*(images/|static/)).*$', index_view, name='index'), 
    re_path(r'^my_app/(?P<path>.*?\.[^/]+)$',serve),
]+ static(MEDIA_URL, document_root=MEDIA_ROOT)
