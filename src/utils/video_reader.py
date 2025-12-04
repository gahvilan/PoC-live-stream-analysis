import cv2

cap = None
actual_frame = 0
frame_count = 0
fps = 0

def frame_to_seconds(frame_number=-1):
    global actual_frame, fps
    
    if frame_number > 0:
        return frame_number / fps
    else:
        return actual_frame /fps

def get_frame_count():
    global frame_count
    return frame_count
    
    
def get_actual_frame():
    global actual_frame
    return actual_frame

def jump_frames(nframes):
    global cap, actual_frame

    if cap:
        actual_frame += nframes
        cap.set(cv2.CAP_PROP_POS_FRAMES, actual_frame)

def read_video(path, start_frame=0):
    global cap, actual_frame,frame_count, fps
    cap = cv2.VideoCapture(path)

    actual_frame = start_frame
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, actual_frame)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        actual_frame += 1

        yield frame

    cap.release()