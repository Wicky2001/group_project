from ultralytics import YOLO
import cv2
import time
from models.utils.util import insert_data_to_data_base,read_license_plate
import datetime

# load models
coco_model = YOLO("../utils/yolov8n.pt")
license_plate_detector = YOLO('../utils/license_plate_detector.pt')

vehicles = [2, 3, 5, 7]

# load video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
number_plate_start_time = time.time()
window_x = 100  # Horizontal position
window_y = 100  # Vertical position
license_plate_text = None
gate_open = False
gate_timer_start = 0
gate_open_duration = 10
count = 0
while True:
    count += 1
    ret, frame = cap.read()
    if not ret:
        break

    # Wait for a key press for 1 millisecond, break the loop if 'q' is pressed

    if not gate_open:
        # detect vehicles
        detections = coco_model(frame)[0]
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            print(detection)
            if int(class_id) in vehicles:
                print("Vehical is detected")

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)

                # Test Code
                # cv2.putText(frame, "Vehical detected", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5,
                #             cv2.LINE_AA)

                # crop thr vehical from the rest of the background
                vehicle_cropped_frame = frame[int(y1):int(y2), int(x1):int(x2)]
                # cv2.imshow("Vehical", vehicle_cropped_frame)

                # detect license plates
                license_plates = license_plate_detector(vehicle_cropped_frame)[0]
                # if no licence plate is detected go to the beginning of the loop
                if len(license_plates.boxes.data.tolist()) == 0:
                    continue

                if len(license_plates.boxes.data.tolist()) > 0:
                    print("License Plates Detected:")

                    # Test Code
                    cv2.putText(frame, "License plate detected", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3,
                                cv2.LINE_AA)

                    for license_plate in license_plates.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = license_plate
                        # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
                        # crop license plate
                        license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                        # process license plate
                        license_plate_crop_grey = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_grey, 64, 255,
                                                                     cv2.THRESH_BINARY_INV)

                        # read license plate number
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

                            current_datetime = datetime.datetime.now()
                            current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
                            # ..\Client\public\detected_vehicles_images
                            image_save_location = f"../../Client/public/detected_vehicles_images/{license_plate_text + current_datetime_str}.jpg"
                            cv2.imwrite(image_save_location, frame)

                            # insert number plate to database
                            insert_data_to_data_base("vehicals", "detections", license_plate_text, "OUT")
                            print("License Plate Text:", license_plate_text)
                            end_time = time.time()
                            elapsed_time = end_time - number_plate_start_time
                            print(f"Elapsed Time: {elapsed_time} seconds")
                            if not gate_open:
                                print("Opening gate...")
                                gate_open = True
                                gate_timer_start = time.time()
                                cv2.imshow('Webcam Video', frame)
                                cv2.moveWindow('Webcam Video', window_x, window_y)
    if not gate_open:
        # Display the frame in a window named 'Webcam Video'
        cv2.imshow('Webcam Video', frame)
        cv2.moveWindow('Webcam Video', window_x, window_y)

    if gate_open and (time.time() - gate_timer_start >= gate_open_duration):
        print("Gate is closed")
        gate_open = False
        gate_timer_start = 0
        number_plate_start_time = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit(0)
