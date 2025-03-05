from ultralytics import YOLO
import math
import cv2
import numpy as np

# 假设内参矩阵（根据你的相机参数调整）
int_mat = np.array([[1.29869001e+03, 0.00000000e+00, 6.27411712e+02],
                    [0.00000000e+00, 1.29810714e+03, 8.63572904e+02],
                    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
# 假设相机高度（单位：米）
cam_H = 1.2

# 假设相机角度（单位：弧度）
angle_a = math.radians(5)  # 例如 10 度的俯仰角
angle_b = math.radians(10)  # 假设没有偏航角

# 载入训练好的模型
model = YOLO("D:\\PythonProject\\OpenCV\\YOLO_BDD100K\\runs\\detect\\train\\weights\\best.pt")

# 读取视频
video_path = "true.mp4"  # 替换为你的视频文件路径
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 获取视频的帧宽度和高度，方便保存时设置输出视频的尺寸
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 创建 VideoWriter 对象，保存结果视频
output_video_path = "output_video_warning.mp4"  # 输出视频路径
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

# 需要警告的标签列表
warning_labels = ['car', 'bus', 'person', 'bike', 'truck', 'motor', 'train', 'rider']

# 计算物体的世界坐标和距离的函数
def object_point_world_position(u, v, h, w, in_mat, angle_a, angle_b):
    fx = in_mat[0, 0]  # 相机的焦距（x 方向）
    fy = in_mat[1, 1]  # 相机的焦距（y 方向）
    cx = in_mat[0, 2]  # 主点的 x 偏移
    cy = in_mat[1, 2]  # 主点的 y 偏移

    # 调整相机的角度
    angle_c = angle_b + angle_a  # 俯仰角和偏航角的组合

    # 将像素坐标 (u, v) 转换为相机坐标系中的归一化坐标 (x, y)
    x_norm = (u - cx) / fx
    y_norm = (v - cy) / fy

    # 假设深度与相机高度和角度有关
    depth = cam_H / math.tan(angle_c)  # 通过相机的俯仰角来计算目标的深度

    # 使用深度值来计算世界坐标 (X, Y, Z)
    X = depth * x_norm
    Y = depth * y_norm
    Z = depth  # 假设 Z 轴是沿着视线方向的

    # 计算距离
    distance = math.sqrt(X ** 2 + Y ** 2 + Z ** 2)

    return distance, (X, Y, Z)

# 循环读取视频帧并进行处理
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame or end of video.")
        break

    # 将当前帧传递给YOLO进行推理
    results = model(frame, device="cuda")

    # 提取结果中的检测框
    bboxes = results[0].boxes.xyxy  # 获取检测框的坐标 (x_min, y_min, x_max, y_max)
    class_ids = results[0].boxes.cls  # 获取每个框的类别id
    scores = results[0].boxes.conf  # 获取每个框的置信度
    names = results[0].names  # 获取类名列表

    for bbox, class_id, score in zip(bboxes, class_ids, scores):
        x_min, y_min, x_max, y_max = bbox
        u, v, w, h = x_min.item(), y_min.item(), x_max.item() - x_min.item(), y_max.item() - y_min.item()

        # 计算物体的距离
        distance, world_position = object_point_world_position(u, v, h, w, int_mat, angle_a, angle_b)

        # 类别名称
        class_name = names[int(class_id)]  # 获取类别名称

        # 判断是否需要警告
        if class_name in warning_labels and distance < 10:
            distance_label = f"{distance:.2f} m  Warning!"  # 显示距离和警告
        else:
            distance_label = f"{distance:.2f} m"  # 显示距离

        # 在框内添加距离和警告
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8  # 适中字体大小
        font_thickness = 2  # 增加字体粗细
        background_color = (0, 0, 0)  # 黑色背景

        # 获取文本的大小和位置
        text_size = cv2.getTextSize(distance_label, font, font_scale, font_thickness)[0]
        text_x = int(x_min + 5)  # 将文本放在框的左上角
        text_y = int(y_min + h / 2)  # 将文本放在框的中心

        # 绘制黑色背景矩形
        cv2.rectangle(frame,
                      (text_x - 5, text_y - text_size[1] - 5),
                      (text_x + text_size[0] + 5, text_y + 5),
                      background_color, -1)  # -1 表示填充矩形

        # 绘制文本
        cv2.putText(frame, distance_label, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

    # 使用 YOLO 绘制检测框和标签
    frame = results[0].plot()  # 这会自动绘制框和标签

    # 写入当前帧到输出视频
    out.write(frame)

    # 显示当前帧
    cv2.imshow("Detection", frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
