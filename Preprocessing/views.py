import os

from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image
import cv2
import numpy as np
from django.conf import settings
from PIL import Image
import io
from django.http import JsonResponse
from django.core.files.storage import default_storage


# Create your views here.
def preprocessing_view(request):
    return render(request, 'preprocessing/processing.html')


def enhancement_view(request):
    return render(request, 'preprocessing/enhancement.html')


def fusion_view(request):
    return render(request, 'preprocessing/fusion.html')


def rotate_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            # 打开图片
            img = Image.open(image_file)
            rotated_img = img.rotate(90, expand=True)

            # 根据原图格式保存（例如：如果上传的是 PNG 图像）
            file_extension = image_file.name.split('.')[-1].lower()
            rotated_image_path = os.path.join(settings.MEDIA_ROOT, 'rotated_image.' + file_extension)

            if file_extension == 'jpg' or file_extension == 'jpeg':
                rotated_img.save(rotated_image_path, 'JPEG')
            elif file_extension == 'png':
                rotated_img.save(rotated_image_path, 'PNG')
            else:
                rotated_img.save(rotated_image_path, 'JPEG')

            # 返回图片 URL
            image_url = settings.MEDIA_URL + 'rotated_image.' + file_extension
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def grayscale_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            # 使用 Pillow 打开图像
            img = Image.open(image_file)

            # 将图像转换为 NumPy 数组，以便 OpenCV 处理
            image = np.array(img)

            # 图像处理：转换为灰度图
            grayscale_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            # 确定文件保存路径
            file_path = os.path.join(settings.MEDIA_ROOT, 'grayscale_image.jpg')

            # 保存图像
            cv2.imwrite(file_path, grayscale_img)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'grayscale_image.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def sharpening_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            # 使用 Pillow 打开图像
            img = Image.open(image_file)

            # 将图像转换为 NumPy 数组，以便 OpenCV 处理
            image = np.array(img)

            # 图像处理：转换为灰度图
            sharpen_kernel = np.array([[0, -1, 0],
                                       [-1, 5, -1],
                                       [0, -1, 0]])
            sharpened_img = cv2.filter2D(image, -1, sharpen_kernel)

            # 确定文件保存路径
            file_path = os.path.join(settings.MEDIA_ROOT, 'sharpened_image.jpg')

            # 保存图像
            cv2.imwrite(file_path, sharpened_img)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'sharpened_image.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def frequency_transform(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            # 使用 Pillow 打开图像
            img = Image.open(image_file)
            # 将图像转换为 NumPy 数组
            image = np.array(img)

            # 如果图像是彩色图像，转换为灰度图
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            # 进行傅里叶变换
            f = np.fft.fft2(image)
            fshift = np.fft.fftshift(f)  # 将低频移到图像中心
            magnitude_spectrum = np.abs(fshift)  # 获取幅度谱

            # 将频域图像的幅度谱转换为可视化的形式
            magnitude_spectrum = np.log(magnitude_spectrum + 1)  # 使用log变换进行增强

            # 转换为图像并保存
            magnitude_spectrum = np.uint8(magnitude_spectrum / np.max(magnitude_spectrum) * 255)
            file_path = os.path.join(settings.MEDIA_ROOT, 'frequency_image.jpg')
            cv2.imwrite(file_path, magnitude_spectrum)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'frequency_image.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def gaussian_blur(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            # 使用 Pillow 打开图像
            img = Image.open(image_file)

            # 将图像转换为 NumPy 数组，以便 OpenCV 处理
            image = np.array(img)

            gauss = cv2.GaussianBlur(image, (5, 5), 0)

            file_path = os.path.join(settings.MEDIA_ROOT, 'gaussian_blur.jpg')

            # 保存图像
            cv2.imwrite(file_path, gauss)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'gaussian_blur.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def binarize_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            # 使用 Pillow 打开图像
            img = Image.open(image_file)
            # 将图像转换为 NumPy 数组
            image = np.array(img)

            # 如果图像是彩色图像，转换为灰度图
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

            # 应用二值化
            _, binarized_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

            # 保存二值化后的图像
            file_path = os.path.join(settings.MEDIA_ROOT, 'binarized_image.jpg')
            cv2.imwrite(file_path, binarized_image)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'binarized_image.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def concatenation(request):
    if request.method == 'POST' and request.FILES.get('image1') and request.FILES.get('image2'):
        image_file1 = request.FILES['image1']
        image_file2 = request.FILES['image2']
        try:
            img1_array = np.frombuffer(image_file1.read(), np.uint8)
            img2_array = np.frombuffer(image_file2.read(), np.uint8)

            # 使用 cv2.imdecode 读取为 OpenCV 图像
            image1 = cv2.imdecode(img1_array, cv2.IMREAD_COLOR)
            image2 = cv2.imdecode(img2_array, cv2.IMREAD_COLOR)
            # 转换为灰度图像
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

            # 使用ORB检测器进行关键点检测与匹配
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(gray1, None)
            kp2, des2 = orb.detectAndCompute(gray2, None)

            # 使用Brute-Force匹配器进行匹配
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)

            # 排序匹配结果
            matches = sorted(matches, key=lambda x: x.distance)

            # 绘制匹配结果
            img_matches = cv2.drawMatches(image1, kp1, image2, kp2, matches[:10], None,
                                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            file_path = os.path.join(settings.MEDIA_ROOT, 'concatenated_image.jpg')
            cv2.imwrite(file_path, img_matches)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'concatenated_image.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})


def concatenation1(request):
    if request.method == 'POST' and request.FILES.get('image1') and request.FILES.get('image2'):
        image_file1 = request.FILES['image1']
        image_file2 = request.FILES['image2']
        try:
            img1_array = np.frombuffer(image_file1.read(), np.uint8)
            img2_array = np.frombuffer(image_file2.read(), np.uint8)

            # 使用 cv2.imdecode 读取为 OpenCV 图像
            image1 = cv2.imdecode(img1_array, cv2.IMREAD_COLOR)
            image2 = cv2.imdecode(img2_array, cv2.IMREAD_COLOR)
            # 转换为灰度图像
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

            fused_img = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)

            fused_img = np.clip(fused_img, 0, 255).astype(np.uint8)

            fused_img_pil = Image.fromarray(cv2.cvtColor(fused_img, cv2.COLOR_BGR2RGB))

            file_path = os.path.join(settings.MEDIA_ROOT, 'concatenated1_image.jpg')
            cv2.imwrite(file_path, fused_img)

            # 返回图像 URL
            image_url = os.path.join(settings.MEDIA_URL, 'concatenated1_image.jpg')
            return JsonResponse({"success": True, "image_url": image_url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "No image uploaded."})
