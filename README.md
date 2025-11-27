# Video Analysis PoC

This Proof of Concept (PoC) processes `.mp4` video files from monitoring cameras and uses **YOLO** to detect people. Additional models and modules can be integrated later to identify **movement**, **clothing**, and other attributes.

---

## 📦 Requirements

Create a Python virtual environment and install dependencies from `requirements.txt`.

The full dependency list is managed in `requirements.txt`. Install everything with:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Project

### **1. Clone the repository**
```bash
git clone <your_repo_url>
cd <project_folder>
```

### **2. Create and activate a virtual environment**

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

---

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

### **4. Prepare your video file**
Place your `.mp4` video anywhere on your machine. When you run the script, you will be prompted to type or paste the full path (you can use paths like `~/Downloads/video.mp4`).

---

### **5. Run the script**
From the project root, with the virtual environment activated:

```bash
python src/main.py
```

The script will ask for the path to the `.mp4` file you want to analyze.

By default it runs in **real-time mode**, opening a window with the processed video. Press `q` while the window is focused to stop playback early.

You can also control behavior explicitly via CLI parameters:

- `--video_path` – optional path to a `.mp4` file. If omitted, the script will prompt you.
- `--mode` – either `realtime` (default) or `frames`.

**Examples:**

- Real-time visualization (prompt for path):

  ```bash
  python src/main.py
  ```

- Real-time visualization (explicit path):

  ```bash
  python src/main.py --video_path "~/Videos/sample.mp4" --mode realtime
  ```

- Save annotated frames for training (no window):

  ```bash
  python src/main.py --video_path "~/Videos/sample.mp4" --mode frames
  ```

  Frames will be written to `output/frames/frame_<index>.jpg`.

---

## 📁 Project Structure

```
project/
│── README.md
│── requirements.txt
│── venv/                  # (optional) Python virtual environment
│── src/
│   ├── main.py            # Entry point; asks for video path and runs analysis
│   ├── config.py          # Basic configuration (e.g., model path, output dirs)
│   ├── detector.py        # YOLO person detector (ultralytics YOLOv8)
│   ├── tracker.py         # Simple ID tracker across frames
│   ├── clothing_classifier.py  # Color-based clothing/vest classifier
│   └── utils/
│       ├── video_reader.py     # Frame generator for a video file
│       └── drawing.py          # Drawing bounding boxes and labels
│
└── output/
    └── frames/            # (optional) folder for saving processed frames if enabled
```

---

## 🧠 How It Works

1. Loads YOLO via **ultralytics**  
2. Processes the video frame-by-frame using **OpenCV**  
3. Detects people and assigns simple tracking IDs  
4. Classifies dominant clothing color (including orange vests) and draws labeled bounding boxes  
5. Displays the annotated video in real time (press `q` to quit)  
6. (Future) Add layers for:
   - Movement tracking  
   - Clothing classification  
   - Pose detection  
   - Behavior analysis  

---

## 🚀 Next Steps

- Integrate **YOLO pose** for movement analysis  
- Add a clothing classifier (ResNet, MobileNet, CLIP-based)  
- Add tracking with **DeepSORT**  
- Add Web UI or dashboard  

---

## 📝 Notes

This PoC is designed for quick iteration. YOLO models can be swapped or extended easily to support additional detection layers.
