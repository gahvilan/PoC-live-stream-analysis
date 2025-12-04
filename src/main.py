import os
import argparse
import cv2
from detector import PersonDetector
from tracker import SimpleTracker
from clothing_classifier import ClothingClassifier
from alertsAPI import AlertService
from intrusionDetector import IntrusionDetector
from utils.video_reader import read_video , jump_frames , get_actual_frame , get_frame_count,frame_to_seconds
from utils.drawing import draw_box
from config import OUTPUT_DIR, MODEL_PATH

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
def draw_progress_bar(frame, current_frame, total_frames,
                      x=50, y=10, width=800, height=12,
                      bar_color=(0,255,0), bg_color=(80,80,80)):
    """
    Draw a progress bar on the frame.
    (x, y) = top-left corner of the bar
    width, height = size of the bar
    """
    # Draw background
    cv2.rectangle(frame, (x, y), (x+width, y+height), bg_color, -1)

    # Calculate filled part
    fill = int((current_frame / total_frames) * width)

    # Draw progress fill
    cv2.rectangle(frame, (x, y), (x+fill, y+height), bar_color, -1)

    return frame
#######################################################
def ask_for_video_path():
    while True:
        path = input("\nEnter the path of the .mp4 video to analyze: ").strip()

        # Expand "~/Downloads/video.mp4"
        path = os.path.expanduser(path)

        if not path.lower().endswith(".mp4"):
            print("❌ Error: File must be an .mp4")
            continue
        
        if not os.path.exists(path):
            print("❌ Error: File not found. Try again.")
            continue

        return path

def main_loop(video_path, service, mode):
    instrusion_area = {    "polygon": [        [400, 50],         [700, 50],
                                    [750, 300], [350, 300]]}
    intrusion = IntrusionDetector(instrusion_area)                     
    detector = PersonDetector(MODEL_PATH)
    tracker = SimpleTracker()
    classifier = ClothingClassifier()

  
    activation =0

    for frame in read_video(video_path, 35000):
        frame = cv2.resize(frame, (1280, 720) )
        persons = detector.detect(frame)
        tracked = tracker.update(persons)

        alerts = intrusion.check_frame(persons)
        #### report active alerts until new are obtained
        if len(alerts) > 0:
            service.set_alerts(alerts)
            activation = 50

        render_frame = intrusion.draw_polygon(frame)
            
        for obj_id, box in tracked.items():
            color = classifier.classify(frame, box)
            draw_box(render_frame, box, obj_id=obj_id, label=color)
        ### render alert for a while
        if activation > 0:
            cv2.circle(render_frame, (1000, 50), 10, (0, 0, 255), -1)
            activation-=1
            
        if mode == "frames":
            cv2.imwrite(f"{OUTPUT_DIR}/frame_{frame_index}.jpg", render_frame)
            frame_index += 1
        else:
            cv2.putText(render_frame,f" {int(frame_to_seconds())} secs: {int(frame_to_seconds(get_frame_count()))}", (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            draw_progress_bar(render_frame , get_actual_frame(),get_frame_count())

            cv2.imshow("Live Analysis", render_frame)

            k = cv2.waitKey(1) 
            if k & 0xFF == ord('q'):
                break
            if k & 0xFF == ord('m'):
                jump_frames(10)
            if k & 0xFF == ord('M'):
                jump_frames(100)
            if k & 0xFF == ord('n'):
                jump_frames(-10)
            if k & 0xFF == ord('N'):
                jump_frames(-100)
                

    if mode != "frames":
        cv2.destroyAllWindows()

################################################################################
def main(video_path: str | None = None, mode: str = "realtime"):
    ensure_dir(OUTPUT_DIR)

   
    # 🔥 Ask user for input
    if not video_path:
        video_path = ask_for_video_path()
    else:
        video_path = os.path.expanduser(video_path)

    print(f"\n📹 Processing video: {video_path} (mode={mode})")
#############################
    
    service = AlertService()
    service.run()

    main_loop(video_path, service, mode)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, default="E:/Resources/Ocasa/2410133_C08_M77R2_2_20251104_095113.mp4")
    parser.add_argument("--mode", type=str, choices=["realtime", "frames"], default="realtime")
    args = parser.parse_args()

    main(video_path=args.video_path, mode=args.mode)
