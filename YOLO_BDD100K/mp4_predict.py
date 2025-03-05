import cv2
from ultralytics import YOLO

# 加载 YOLOv8 模型
# model = YOLO("yolov8n.pt")
model = YOLO("D:\\PythonProject\\OpenCV\\YOLO_BDD100K\\runs\\detect\\train\\weights\\last.pt")


# 打开视频文件
input_path = "true.mp4"
output_path = "output.mp4"
cap = cv2.VideoCapture(input_path)

if not cap.isOpened():
    print("Error: Unable to open video file or device.")
    exit()

# 获取视频属性
fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 视频宽度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频高度
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码格式

# 初始化视频写入对象
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

title = "YOLOv8 Inference"
cv2.namedWindow(title, cv2.WINDOW_NORMAL)
cv2.moveWindow(title, 200, 200)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        # 推理
        results = model(frame)
        annotated_frame = results[0].plot()

        # 显示结果
        cv2.imshow(title, annotated_frame)

        # 写入到输出视频文件
        out.write(annotated_frame)

        # 按下“q”退出
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
    else:
        break

# 释放资源
cap.release()
out.release()  # 释放写入对象
cv2.destroyAllWindows()
