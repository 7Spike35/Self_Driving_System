# urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # 确保引用正确的 views 模块

urlpatterns = [
    # 页面视图
    path('Identification/', views.Identification, name='Identification'),
    path('lane/', views.lane, name='lane'),
    path('target/', views.target, name='target'),
    path('warning/', views.warning, name='warning'),

    # 视频上传与处理
    path('upload/', views.upload_video, name='upload_video'),
    path('process_video/', views.process_video, name='process_video'),

    # 视频流显示
    path('video_stream/<str:video_name>/', views.stream_video, name='video_stream'),

    # 管理后台
    path('admin/', admin.site.urls),
]

# 配置静态文件和媒体文件的URL处理
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

