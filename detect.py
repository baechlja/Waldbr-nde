from ultralytics import YOLO

model = YOLO("runs/detect/train9/weights/best.pt")

results = model("test.jpg")

for r in results:
    for c in r.boxes.cls:
        print(model.names[int(c)])