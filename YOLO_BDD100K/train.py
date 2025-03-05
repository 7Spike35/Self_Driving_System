import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

from ultralytics import YOLO


def main():

    model = YOLO("yolov8n.pt")

    model.train(data="F:/BDD100K/data.yaml", epochs=5, imgsz=320, batch=4)

if __name__ == "__main__":
    main()