import threading
import cv2
import datetime as time
from flask import Flask, Response
from ultralytics import YOLO
from models.utils.util import insert_data_to_data_base, read_license_plate

# Global variables for detection and streaming
stop_detection_thread = False
stop_stream_thread = False
latest_frame = None
lock = threading.Lock()

# Function for vehicle detection
def vehicle_detection_process(coco_model, license_plate_detector):
    global stop_detection_thread, latest_frame

    vehicles = [2, 3, 5, 7]  # Vehicle class IDs

    # Load video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    gate_open = False
    gate_timer_start = 0
    gate_open_duration = 10

    while not stop_detection_thread:
        ret, frame = cap.read()
        if not ret:
            break

        # Always update the frame for streaming, regardless of detection
        with lock:
            latest_frame = frame.copy()

        # Perform vehicle detection
        detections = coco_model(frame)[0]
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

                vehicle_cropped_frame = frame[int(y1):int(y2), int(x1):int(x2)]
                license_plates = license_plate_detector(vehicle_cropped_frame)[0]

                for license_plate in license_plates.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = license_plate
                    license_plate_crop = frame[int(y1)-20:int(y2)+20, (int(x1) + 50):int(x2), :]

                    if not license_plate_crop.any():
                        continue

                    license_plate_crop_grey = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    license_plate_crop_thresh = cv2.adaptiveThreshold(
                        license_plate_crop_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY_INV, 21, 30)

                    license_plate_text, _ = read_license_plate(license_plate_crop_thresh)

                    # Add the detected license plate text on the frame
                    if license_plate_text is not None:
                        cv2.putText(frame, f"License Plate: {license_plate_text}", (150, 80),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 1, cv2.LINE_AA)

                        if not gate_open:
                            gate_open = True
                            gate_timer_start = time.time()

        if gate_open and (time.time() - gate_timer_start >= gate_open_duration):
            gate_open = False
            gate_timer_start = 0

        # Optional: Display the frame locally (for debugging)
        cv2.imshow('Webcam Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_detection_thread = True

    cap.release()
    cv2.destroyAllWindows()

# Function to generate video frames for streaming
def generate_frames():
    global latest_frame, stop_stream_thread

    while not stop_stream_thread:
        with lock:
            if latest_frame is not None:
                frame = latest_frame.copy()

                # Convert frame to JPEG and yield it for streaming
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Flask application
