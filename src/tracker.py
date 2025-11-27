import math

class SimpleTracker:
    def __init__(self, max_distance=50):
        self.next_id = 1
        self.objects = {}  # id -> (x1, y1, x2, y2)
        self.max_distance = max_distance

    def _center(self, box):
        x1, y1, x2, y2 = box
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def _distance(self, b1, b2):
        c1 = self._center(b1)
        c2 = self._center(b2)
        return math.dist(c1, c2)

    def update(self, detections):
        assigned = {}
        updated_ids = {}

        # Assign existing IDs
        for obj_id, old_box in self.objects.items():
            best_match = None
            best_distance = float("inf")

            for det in detections:
                distance = self._distance(old_box, det[:4])
                if distance < best_distance and distance < self.max_distance:
                    best_distance = distance
                    best_match = det

            if best_match:
                updated_ids[obj_id] = best_match[:4]
                assigned[id(best_match)] = True
        
        # Create new IDs for unassigned detections
        for det in detections:
            if id(det) not in assigned:
                updated_ids[self.next_id] = det[:4]
                self.next_id += 1

        self.objects = updated_ids
        return self.objects