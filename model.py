from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # leve e rápido

model.train(
    data="dataset/silksong/data.yaml",
    epochs=150,
    imgsz=640,
    batch=8,
    workers=0,
    name="silksong_yolo",
)
