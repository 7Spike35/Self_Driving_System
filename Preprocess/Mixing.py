import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 读取两张图像
img1 = cv2.imread('0_left.jpg')
img2 = cv2.imread('0_right.jpg')

# 确保两张图像大小相同
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# 图像融合：加权平均法
alpha = 0.5  # 第一个图像的权重
beta = 1 - alpha  # 第二个图像的权重
fused_img = cv2.addWeighted(img1, alpha, img2, beta, 0)

# 对融合后的图像进行归一化，确保像素值在[0, 255]范围内
fused_img = np.clip(fused_img, 0, 255).astype(np.uint8)

# 转换为PIL格式以便显示
fused_img_pil = Image.fromarray(cv2.cvtColor(fused_img, cv2.COLOR_BGR2RGB))

# 显示图像
plt.figure(figsize=(6, 6))
plt.imshow(fused_img_pil)
plt.title("Fused Image (Weighted Average)")
plt.axis('off')
plt.show()

