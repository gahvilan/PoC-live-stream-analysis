from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        """
        Returns YOLO detection results containing bounding boxes for persons only.
        """
        results = self.model(frame)[0]
        persons = []

        for box in results.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # Class 0 = person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                persons.append((x1, y1, x2, y2, conf))

        return persons