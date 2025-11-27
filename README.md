# Video Analysis PoC

This Proof of Concept (PoC) processes `.mp4` video files from monitoring cameras and uses **YOLO** to detect people. Additional models and modules can be integrated later to identify **movement**, **clothing**, and other attributes.

---

## 📦 Requirements

Create a Python virtual environment and install dependencies from `requirements.txt`.

### **requirements.txt**
```
ultralytics
opencv-python
numpy
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

### **4. Add your video file**
Place your `.mp4` video inside the `videos/` folder (create it if it doesn’t exist).

---

### **5. Run the script**
```bash
python main.py --video_path videos/sample.mp4
```

---

## 📁 Project Structure

```
project/
│── main.py
│── requirements.txt
│── README.md
│── videos/
│     └── sample.mp4
│── output/
       └── processed_<timestamp>.mp4
```

---

## 🧠 How It Works

1. Loads YOLO via **ultralytics**  
2. Processes the video frame-by-frame using **OpenCV**  
3. Detects people  
4. Draws bounding boxes and exports processed output  
5. (Future) Add layers for:
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
