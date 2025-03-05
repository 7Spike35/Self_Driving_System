from django.urls import path

from .views import index
from Identification.views import hello_world


urlpatterns=[
    path('index/',index,name='index'),
    path('helloworld/',hello_world,name='helloworld')
]