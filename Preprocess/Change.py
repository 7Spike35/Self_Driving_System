import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 加载图像
img = Image.open("AAB_3741.jpg")
img = np.array(img)  # 转为numpy数组

# 确保图像数据在0到255的范围内（整数类型）
img = np.clip(img, 0, 255).astype(np.uint8)

# 进行几何变换（旋转90度）
rotated_img = np.rot90(img)

# 频域变换（傅里叶变换）
f_transform = np.fft.fft2(img)
f_shifted = np.fft.fftshift(f_transform)  # 移动零频率到中心

# 计算幅度谱并进行归一化
magnitude_spectrum = np.abs(f_shifted)
magnitude_spectrum = np.log(magnitude_spectrum + 1)  # 对数变换
magnitude_spectrum = np.clip(magnitude_spectrum, 0, np.max(magnitude_spectrum))  # 归一化到最大值

# 将幅度谱归一化到[0, 1]范围（适用于imshow）
magnitude_spectrum = magnitude_spectrum / np.max(magnitude_spectrum)

# 显示图像
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(rotated_img)
plt.title("Rotated Image")
plt.subplot(1, 2, 2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title("Magnitude Spectrum")
plt.show()
