import cv2
import numpy as np
import matplotlib.pyplot as plt

# 加载两张图片
img1 = cv2.imread("image1.jpg")
img2 = cv2.imread("image2.jpg")

# 转换为灰度图像
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 使用ORB检测器进行关键点检测与匹配
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

# 使用Brute-Force匹配器进行匹配
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# 排序匹配结果
matches = sorted(matches, key = lambda x:x.distance)

# 绘制匹配结果
img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# 显示图像
plt.imshow(img_matches)
plt.title("Image Matching")
plt.show()
