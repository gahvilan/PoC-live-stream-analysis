import cv2
import numpy as np

class ClothingClassifier:
    COLORS = {
        "red": ((0, 50, 20), (10, 255, 255)),
        "orange": ((10, 50, 20), (20, 255, 255)),
        "blue": ((90, 50, 20), (130, 255, 255)),
        "green": ((40, 50, 20), (80, 255, 255)),
        "yellow": ((20, 50, 20), (35, 255, 255)),
        "black": ((0, 0, 0), (180, 255, 40)),
        "white": ((0, 0, 200), (180, 40, 255))
    }

    def classify(self, frame, box):
        x1, y1, x2, y2 = box
        crop = frame[y1:y2, x1:x2]
        
        if crop.size == 0:
            return "unknown"

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

        counts = {k: 0 for k in self.COLORS}

        for color, (lower, upper) in self.COLORS.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            counts[color] = cv2.countNonZero(mask)

        return max(counts, key=counts.get)