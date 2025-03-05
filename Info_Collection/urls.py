# from django.urls import path
# from. import views
#
# urlpatterns = [
#     path('info_collection/', views.info_collection_view, name='info_collection'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    # 数据采集页面
    path('info_collection/', views.info_collection_view, name='info_collection'),

    # 视频流（摄像头视频流）
    path('video_feed/', views.video_feed, name='video_feed'),

    # 上传视频文件
    path('upload/', views.upload_video, name='upload_video'),
]
