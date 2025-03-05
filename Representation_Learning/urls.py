from django.urls import path

from .views import re_learn


urlpatterns=[
    path('re_learn/',re_learn,name='re_learn')
]