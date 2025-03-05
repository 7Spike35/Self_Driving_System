# from django.http import HttpResponse, StreamingHttpResponse
# import subprocess
#
# # Create your views here.
# from django.shortcuts import render,redirect
# import os
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
#
# from .forms import VideoForm
#
# def Identification(request):
#     return render(request,'Identification.html')
# def hello_world(request):
#     return HttpResponse("Hello, World!")
#
# def lane(request):
#     return render(request,'lane.html')
# def target(request):
#     return render(request,'target.html')
# def warning(request):
#     return render(request,'warning.html')
#
#
# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('Identification')
#     else:
#         form = VideoForm()
#     return render(request, 'upload.html', {'form': form})
#
# from django.http import JsonResponse
# from django.conf import settings
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
from django.urls import reverse
def process_video(request):
    if request.method == 'POST':
        try:
            # 从前端接收文件
            video_file = request.FILES.get('video_file')
            if not video_file:
                return JsonResponse({'success': False, 'error': '未提供视频文件'})

            # 保存视频到指定路径
            upload_path = os.path.join(settings.MEDIA_ROOT, 'upload', video_file.name)
            with open(upload_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            # 定义输出路径
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'{video_file.name}')

            # 处理方法和命令
            command = ['python', 'D:\\PythonProject\\OpenCV\\YOLOP\\tools\\demo.py', '--source', upload_path, '--save-dir', output_dir]
            # subprocess.run(command, check=True)

            # 返回处理后的视频 URL
    #         output_url = f'{settings.MEDIA_URL}output/{video_file.name}'
    #         return JsonResponse({'success': True, 'output_video_url': output_url})
    #
    #     except Exception as e:
    #         return JsonResponse({'success': False, 'error': str(e)})
    # return JsonResponse({'success': False, 'error': '请求方法错误'})
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
            # 脚本执行失败，返回错误信息
                return JsonResponse({
                    'success': False,
                    'error': '视频处理脚本执行失败',
                    'details': result.stderr
                })

            # 使用 reverse 获取 stream_video 的URL
            stream_video_url = reverse('video_stream', args=[video_file.name])

        # 返回处理后的视频 URL
            return JsonResponse({
                'success': True,
                'output_video_url': stream_video_url,
                'message': '视频处理成功'
            })

        except subprocess.CalledProcessError:
            return JsonResponse({'success': False, 'error': '视频处理脚本执行失败'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        return JsonResponse({'success': False, 'error': '请求方法错误'})

#
#
#
# def stream_video(request, video_name):
#     # 获取视频文件路径
#     video_path = os.path.join(settings.MEDIA_ROOT, 'output', video_name)
#
#     # 检查文件是否存在
#     if not os.path.exists(video_path):
#         return HttpResponse('Video not found', status=404)
#
#     # 打开视频文件并创建视频流响应
#     with open(video_path, 'rb') as video_file:
#         def video_stream_generator():
#             while True:
#                 chunk = video_file.read(4096)  # 每次读取4KB
#                 if not chunk:
#                     break
#                 yield chunk
#
#         response = StreamingHttpResponse(video_stream_generator(), content_type='video/mp4')
#         return response

# views.py

import os
import subprocess
import sys
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.conf import settings
from .forms import VideoForm
from django.core.files.storage import FileSystemStorage


# 显示页面视图
def Identification(request):
    return render(request, 'Identification.html')


def hello_world(request):
    return HttpResponse("Hello, World!")


def lane(request):
    return render(request, 'lane.html')


def target(request):
    return render(request, 'target.html')


def warning(request):
    return render(request, 'warning.html')


# 上传视频视图
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Identification')
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})


# 保存上传的视频文件
def save_video_file(video_file):
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'upload'))
    filename = fs.save(video_file.name, video_file)
    file_path = fs.path(filename)
    return file_path


# 处理视频（调用外部处理脚本进行处理）
# def process_video(request):
#     if request.method == 'POST':
#         try:
#             # 获取上传的视频文件
#             video_file = request.FILES.get('video_file')
#             if not video_file:
#                 return JsonResponse({'success': False, 'error': '未提供视频文件'})
#
#             # 保存视频文件
#             upload_path = save_video_file(video_file)
#
#             # 定义输出路径
#             output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
#             os.makedirs(output_dir, exist_ok=True)
#             output_file = os.path.join(output_dir, f'{video_file.name}')
#
#             # 执行处理命令，使用相对路径和当前 Python 解释器
#             script_path = os.path.join(settings.BASE_DIR, 'OpenCV', 'YOLOP', 'tools', 'demo.py')
#             command = [sys.executable, script_path, '--source', upload_path, '--save-dir', output_dir]
#             subprocess.run(command, check=True)
#
#             # 返回处理后的视频 URL
#             output_url = f'{settings.MEDIA_URL}output/{video_file.name}'
#             return JsonResponse({'success': True, 'output_video_url': output_url, 'message': '视频处理成功'})
#
#         except subprocess.CalledProcessError:
#             return JsonResponse({'success': False, 'error': '视频处理脚本执行失败'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return JsonResponse({'success': False, 'error': '请求方法错误'})


# 视频流视图，用于显示处理后的视频
def stream_video(request, video_name):
    video_path = os.path.join(settings.MEDIA_ROOT, 'output', video_name)

    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        return HttpResponse('Video not found', status=404)

    # 打开视频文件并创建视频流响应
    with open(video_path, 'rb') as video_file:
        def video_stream_generator():
            while True:
                chunk = video_file.read(4096)  # 每次读取4KB
                if not chunk:
                    break
                yield chunk

        response = StreamingHttpResponse(video_stream_generator(), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(video_path)
        response['Content-Disposition'] = f'inline; filename={video_name}'
        return response