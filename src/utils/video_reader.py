import cv2

def read_video(path, start_frame = 0):
    cap = cv2.VideoCapture(path)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()