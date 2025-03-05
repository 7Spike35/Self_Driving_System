import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance

# 读取图像
img = cv2.imread('AAB_3741.jpg')

# 1. 直方图均衡化
# 将图像从BGR转为灰度图像
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
equalized_img = cv2.equalizeHist(gray_img)

# 2. Gamma校正
# Gamma值的调整
gamma = 1.5  # Gamma值>1时变亮，<1时变暗
gamma_corrected_img = np.array(255 * (img / 255) ** gamma, dtype='uint8')

# 3. 锐化
# 使用锐化内核
sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
sharpened_img = cv2.filter2D(img, -1, sharpen_kernel)

# 将处理后的图像转换为PIL格式，以便在matplotlib中显示
equalized_img_pil = Image.fromarray(equalized_img)
gamma_corrected_img_pil = Image.fromarray(gamma_corrected_img)
sharpened_img_pil = Image.fromarray(sharpened_img)

# 显示原始图像和增强后的图像
plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(equalized_img_pil, cmap='gray')
plt.title("Histogram Equalization")
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(gamma_corrected_img_pil)
plt.title("Gamma Correction")
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(cv2.cvtColor(np.array(sharpened_img_pil), cv2.COLOR_BGR2RGB))
plt.title("Sharpened Image")
plt.axis('off')

plt.show()
