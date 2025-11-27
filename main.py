from ultralytics import YOLO
import cv2

# Cargar modelo de pose (puede ser yolov8n-pose, yolov8s-pose, yolov8m-pose o YOLO11)
model = YOLO("yolov8l-pose.pt")   # liviano y rápido
# model = YOLO("yolo11n-pose.pt") # si quieres usar la nueva versión YOLO11

# Abrir cámara o video
cap = cv2.VideoCapture("./2410133_C07_M77R2_3_20251103_110000.mp4")  # cambiar a ruta de video si querés

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w = frame.shape[:2]
    frame = cv2.resize(frame, (w//2, h//2))
    # Ejecutar inferencia
    results = model(frame)

    # Dibujar keypoints y skeleton en la imagen
    annotated = results[0].plot()

    # Mostrar
    cv2.imshow("Pose detection", annotated)

    # salir con ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
