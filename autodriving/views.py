import subprocess
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import StreamingHttpResponse
import os

# views.py
from django.http import StreamingHttpResponse

def stream_video(request, video_name):
    # 打开视频文件并创建视频流响应
    with open(video_name, 'rb') as video_file:
        def video_stream_generator():
            while True:
                chunk = video_file.read(4096)
                if not chunk:
                    break
                yield chunk
        response = StreamingHttpResponse(video_stream_generator(), content_type='video/mp4')
        return response


# views.py
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings


# def upload_video(request):
#     if request.method == 'POST':
#         # 获取上传的视频文件
#         video_file = request.FILES.get('video_file')
#         if video_file:
#             # 保存视频文件到服务器
#             video_path = save_video_file(video_file)  # 假设这是你的保存视频文件的函数
#
#             # 生成视频流的URL
#             video_url = request.build_absolute_uri(reverse('video_stream', kwargs={'video_name': video_path}))
#
#             # 返回包含视频URL的响应
#             return JsonResponse({'video_url': video_url})
#         else:
#             return JsonResponse({'error': 'No video file provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
#
#
# def save_video_file(video_file):
#     # 保存视频文件到服务器的某个位置，并返回文件路径
#     # 这里只是一个示例，你需要根据实际情况实现文件保存逻辑
#     file_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
#     with open(file_path, 'wb+') as destination:
#         for chunk in video_file.chunks():
#             destination.write(chunk)
#     return file_path
#
#
# def process_video(request):
#     if request.method == 'POST':
#         try:
#             # 从前端接收文件
#             video_file = request.FILES.get('video_file')
#             if not video_file:
#                 return JsonResponse({'success': False, 'error': '未提供视频文件'})
#
#             # 保存视频到指定路径
#             upload_path = os.path.join(settings.MEDIA_ROOT, 'upload',video_file.name)
#             with open(upload_path, 'wb') as f:
#                 for chunk in video_file.chunks():
#                     f.write(chunk)
#
#             # 定义输出路径
#             output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
#             os.makedirs(output_dir, exist_ok=True)
#             output_file = os.path.join(output_dir, f'{video_file.name}')
#
#             # 处理方法和命令
#             command = ['python', 'D:\\PythonProject\\OpenCV\\YOLOP\\tools\\demo.py', '--source', 'D:\\PythonProject\\autodriving1\\media\\upload', '--save-dir', output_dir]
#
#
#             # 执行 demo.py
#             subprocess.run(command, check=True)
#
#             # 返回处理后的视频 URL
#             output_url = f'/media/output/{video_file.name}'
#             return JsonResponse({'success': True, 'output_video_url': output_url})
#
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return JsonResponse({'success': False, 'error': '请求方法错误'})