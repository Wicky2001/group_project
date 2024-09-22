import os
from datetime import datetime
import cv2
import time
from models.utils.util import read_license_plate, insert_data_to_data_base


# Function for vehicle detection
def vehicle_detection_process(coco_model, license_plate_detector, latest_frame, lock, stop_detection_thread,socketio):
    vehicles = [2, 3, 5, 7]  # Vehicle class IDs
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    gate_open = False
    gate_timer_start = 0
    gate_open_duration = 10

    while not stop_detection_thread():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform vehicle detection and drawing before updating latest_frame
        with lock:
            detections = coco_model(frame)[0]
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                print(detection)
                if int(class_id) in vehicles:
                    print("Vehical is detected")
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

                    vehicle_cropped_frame = frame[int(y1):int(y2), int(x1):int(x2)]
                    license_plates = license_plate_detector(vehicle_cropped_frame)[0]
                    if len(license_plates.boxes.data.tolist()) == 0:
                        continue

                    if len(license_plates.boxes.data.tolist()) > 0:
                        # print("License Plates Detected:")

                        # Test Code
                        cv2.putText(frame, "License plate detected", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),
                                    3,
                                    cv2.LINE_AA)

                    for license_plate in license_plates.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = license_plate
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
                        license_plate_crop = frame[int(y1)-20:int(y2)+20, (int(x1) + 50):int(x2), :]

                        if not license_plate_crop.any():
                            continue


                        license_plate_crop_grey = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        license_plate_crop_thresh = cv2.adaptiveThreshold(
                            license_plate_crop_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY_INV, 21, 30)

                        license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                        if license_plate_text is not None:
                            cv2.putText(frame, "Waiting for Gate to Close", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 0, 0), 1,
                                        cv2.LINE_AA)
                            cv2.putText(frame, f"License Plate: {license_plate_text}", (150, 80),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                        (0, 0, 255), 1,
                                        cv2.LINE_AA)

                            # save captured vehical image to database

                            current_datetime = datetime.now()
                            current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
                            # ..\Client\public\detected_vehicles_images
                            save_dir = os.path.abspath(r"C:\Users\Wicky\Documents\GitHub\group_project_code\API\storage\detected_vehicles_images")
                            if not os.path.exists(save_dir):
                                os.makedirs(save_dir)

                            # Generate the file name with the current date and time
                            current_datetime = datetime.now()
                            current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
                            file_name = f"{license_plate_text + current_datetime_str}.jpg"
                            url_name = f"http://127.0.0.1:5002/images/{license_plate_text + current_datetime_str}.jpg"

                            # Full path for saving the image
                            image_save_location = os.path.join(save_dir, file_name)

                            # Save the image
                            success = cv2.imwrite(image_save_location, license_plate_crop_thresh)
                            if success:
                                print(f"Image saved successfully at: {image_save_location}")
                            else:
                                print(f"Failed to save the image at: {image_save_location}")

                            # insert number plate to database
                            insert_data_to_data_base("vehicals", "detections", license_plate_text, "IN",image_url=url_name,socketio=socketio)
                            # print("License Plate Text:", license_plate_text)
                            latest_frame[0] = frame.copy()
                            time.sleep(5)

            # Update latest_frame after drawing
            latest_frame[0] = frame.copy()

    cap.release()
