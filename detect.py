from ultralytics import YOLO

def detect_fire(path_to_model: str, path_to_image: str) -> str :

    model = YOLO(path_to_model)

    results = model(path_to_image)

    detected_classes = []
    for r in results:
        for c in r.boxes.cls:
            if model.names[int(c)] == "fire":
                print("!"*20, "FIRE DETECTED", "!"*20)
                return True
            else:
                continue
    

if __name__ == "__main__":

    model_path = "/home/projects/waldbraende/runs/detect/train9/weights/best.pt"
    test_image = "/home/projects/waldbraende/test.jpg"

    detect_fire(path_to_model=model_path, path_to_image = test_image)
