import cv2
import numpy as np
import glob

# 棋盘格尺寸 (内部角点数目)
chessboard_size = (8, 5)  # 根据你的棋盘格实际设置
square_size = 3.2  # 每个格子的实际边长（单位：如厘米）

# 准备棋盘格的世界坐标（z=0）
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# 存储所有棋盘格角点
obj_points = []  # 3D 世界坐标
img_points = []  # 2D 图像坐标

# 读取图像文件
images = glob.glob("calibration_images/*.png")  # 替换为你的图片路径
if len(images) == 0:
    print("未找到棋盘格图片，请检查文件路径。")
else:
    print(f"找到 {len(images)} 张图片。")

for fname in images:
    img = cv2.imread(fname)

    if img is None:
        print(f"加载图片失败: {fname}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 找到棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        print(f"在图片 {fname} 中找到角点。")
        obj_points.append(objp)
        img_points.append(corners)

        # 可视化角点
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Chessboard Corners', img)
        cv2.waitKey(500)
    else:
        print(f"未能在图片 {fname} 中找到角点。")

cv2.destroyAllWindows()

# 检查是否有有效的图像和角点
if len(obj_points) == 0 or len(img_points) == 0:
    print("没有有效的角点数据，无法进行标定。")
else:
    # 相机标定
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, gray.shape[::-1], None, None
    )

    # 打印内参矩阵和畸变系数
    print("Camera Matrix (内参矩阵):")
    print(camera_matrix)

    print("\nDistortion Coefficients (畸变系数):")
    print(dist_coeffs)

    # 保存结果
    np.save("camera_matrix.npy", camera_matrix)
    np.save("dist_coeffs.npy", dist_coeffs)

    # 验证重投影误差
    mean_error = 0
    for i in range(len(obj_points)):
        img_points2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
        error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
        mean_error += error

    print("\nMean Reprojection Error:", mean_error / len(obj_points))
