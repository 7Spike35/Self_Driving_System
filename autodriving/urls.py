"""
URL configuration for autodriving project.

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
import sys

from django.conf import settings
from django.conf.urls.static import static

from .views import stream_video

sys.path.append('D:\pytorchusetrue\\autodriving1\\autodriving')
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from home import views as views1
from . import views
from django.urls import path




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views1.index,name='index'),
    path('',include('home.urls')),
    path('',include('Identification.urls')),
    path('',include('Representation_Learning.urls')),
    path('Info_Collection/', include('Info_Collection.urls')),
    path('preprocessing/', include('Preprocessing.urls')),
    # path('upload_video/', views.upload_video, name='upload_video'),
    # path('video_stream/<str:video_name>/', stream_video, name='video_stream'),
    # path('process_video/', views.process_video, name='process_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)