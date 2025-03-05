import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse
import os

# 视图：显示数据采集页面
def info_collection_view(request):
    return render(request, 'info_collection.html')

# 生成视频流（来自摄像头或视频文件）
def generate_video_stream(source=0):
    cap = cv2.VideoCapture(source)  # 如果 source 为 0，则为摄像头，如果为文件路径，则读取文件
    if not cap.isOpened():
        return None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

# 摄像头视频流视图（此视图为实时视频流）
def video_feed(request):
    return StreamingHttpResponse(generate_video_stream(0), content_type='multipart/x-mixed-replace; boundary=frame')

# 上传视频文件视图
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        save_path = os.path.join('media', uploaded_file.name)
        with open(save_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        return render(request, 'upload_complete.html', {'file_url': save_path})
    return render(request, 'info_collection.html')
