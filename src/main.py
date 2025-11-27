import os
import argparse
import cv2
from detector import PersonDetector
from tracker import SimpleTracker
from clothing_classifier import ClothingClassifier
from utils.video_reader import read_video
from utils.drawing import draw_box
from config import OUTPUT_DIR, MODEL_PATH

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

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

def main(video_path: str | None = None, mode: str = "realtime"):
    ensure_dir(OUTPUT_DIR)

    # 🔥 Ask user for input
    if not video_path:
        video_path = ask_for_video_path()
    else:
        video_path = os.path.expanduser(video_path)

    print(f"\n📹 Processing video: {video_path} (mode={mode})")

    detector = PersonDetector(MODEL_PATH)
    tracker = SimpleTracker()
    classifier = ClothingClassifier()

    frame_index = 0

    for frame in read_video(video_path):
        persons = detector.detect(frame)
        tracked = tracker.update(persons)

        for obj_id, box in tracked.items():
            color = classifier.classify(frame, box)
            draw_box(frame, box, obj_id=obj_id, label=color)

        if mode == "frames":
            cv2.imwrite(f"{OUTPUT_DIR}/frame_{frame_index}.jpg", frame)
            frame_index += 1
        else:
            cv2.imshow("Live Analysis", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    if mode != "frames":
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, default=None)
    parser.add_argument("--mode", type=str, choices=["realtime", "frames"], default="realtime")
    args = parser.parse_args()

    main(video_path=args.video_path, mode=args.mode)
