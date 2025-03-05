from ultralytics import YOLO
import math
import cv2
import numpy as np

# 载入训练好的模型
model = YOLO("D:\\PythonProject\\OpenCV\\YOLO_BDD100K\\runs\\detect\\train\\weights\\best.pt")

# 推理多张图像
results = model(["img.jpg"], device="cuda")


for iter, result in enumerate(results):
    result.save(filename=f"result{iter}.jpg")
