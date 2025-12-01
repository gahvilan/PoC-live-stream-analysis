import json
import cv2
import numpy as np

def box_intersects(boxA, boxB):
    """
    boxA and boxB are dicts or tuples: (x1,y1,x2,y2)
    Returns True if boxes overlap.
    """

    Ax1, Ay1, Ax2, Ay2 = boxA
    Bx1, By1, Bx2, By2 = boxB

    # Compute overlap
    inter_x1 = max(Ax1, Bx1)
    inter_y1 = max(Ay1, By1)
    inter_x2 = min(Ax2, Bx2)
    inter_y2 = min(Ay2, By2)

    # Check if valid intersection
    return inter_x2 > inter_x1 and inter_y2 > inter_y1
class IntrusionDetector:
    def __init__(self, json_data):
        """
        JSON must contain:
        {
            "polygon": [[x1,y1], [x2,y2], ...]
        }
        """
      
        # Store polygon as numpy contour
        self.poly = np.array(json_data["polygon"], dtype=np.float32).reshape((-1, 1, 2))
        self.intrusions = []

    def _bbox_to_contour(self, det):
        """
        Convert axis-aligned bbox to contour for intersection.
        """
        x1, y1, x2, y2 = det[0], det[1], det[2], det[3]
        contour = np.array([
            [x1, y1],
            [x2, y1],
            [x2, y2],
            [x1, y2]
        ], dtype=np.int).reshape((-1, 1, 2))
        return contour

     # --------------------------------------------------------
    # NEW METHOD: Draw polygon on frame (with alpha blending)
    # --------------------------------------------------------
    def draw_polygon(self, frame, color=(0, 255, 0), thickness=2, alpha=0.4, fill=False):
        """
        Draws the polygon on the frame.
        color: BGR
        thickness: border thickness
        alpha: transparency (0–1)
        fill: if True, polygon is filled with color
        """

        overlay = frame.copy()
        rect = cv2.boundingRect(self.poly)

        cv2.rectangle(overlay, (rect[0], rect[1]), (rect[2], rect[3]), (100, 250, 100), 3)

        # Alpha blending
        return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    def check_frame(self, detections, frame_id=None):
        """
        detections: list of dicts with x1,y1,x2,y2,class,conf
        Returns intrusions in this frame.
        """

        frame_intrusions = []

        for det in detections:
            x1, y1, x2,y2, conf = (det)
            rect = cv2.boundingRect(self.poly)

            # intersection area between convex polygons
          
            if box_intersects((x1,y1,x2,y2), rect) > 0:  # retval = area of intersection
                event = {"frame": frame_id, "detection": det}
                self.intrusions.append(event)
                frame_intrusions.append(event)

        return frame_intrusions

    def get_intrusions(self):
        return self.intrusions
