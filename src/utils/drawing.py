import cv2

def draw_box(frame, box, obj_id=None, label=None):
    x1, y1, x2, y2 = box
    color = (0, 255, 0)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    text = ""
    if obj_id is not None:
        text += f"ID {obj_id} "
    if label:
        text += f"{label}"

    if text:
        cv2.putText(frame, text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)