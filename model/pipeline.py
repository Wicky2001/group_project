def detector():
    from ultralytics import YOLO
    import cv2
    import time
    from .util import read_license_plate, insert_data_to_data_base

    # load models
    license_plate_detector = YOLO(r'D:\testig\model\license_plate_detector.pt')

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
    while True:
        # Display the frame in a window named 'Webcam Video'
        ret, frame = cap.read()
        if not ret:
            break
        if gate_open:
            cv2.putText(frame, "Waiting for Gate to Close", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1,
                        cv2.LINE_AA)
            cv2.putText(frame, f"License Plate: {license_plate_text}", (150, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 255), 1,
                        cv2.LINE_AA)
        # Wait for a key press for 1 millisecond, break the loop if 'q' is pressed
        cv2.imshow('Webcam Video', frame)
        cv2.moveWindow('Webcam Video', window_x, window_y)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit(0)

        if not gate_open:
            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            # if no licence plate is detected go to the beging of the loop
            if len(license_plates.boxes.data.tolist()) == 0:
                continue

            if len(license_plates.boxes.data.tolist()) > 0:
                print("License Plates Detected:")

            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                # crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                # process license plate
                license_plate_crop_grey = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_grey, 64, 255, cv2.THRESH_BINARY_INV)

                # read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                if license_plate_text is not None:
                    # insert number plate to database
                    insert_data_to_data_base("vehicals", "detections", license_plate_text)
                    print("License Plate Text:", license_plate_text)
                    end_time = time.time()
                    elapsed_time = end_time - number_plate_start_time
                    print(f"Elapsed Time: {elapsed_time} seconds")
                    if not gate_open:
                        print("Opening gate...")
                        gate_open = True
                        gate_timer_start = time.time()

        if gate_open and (time.time() - gate_timer_start >= gate_open_duration):
            print("Gate is closed")
            gate_open = False
            gate_timer_start = 0
            number_plate_start_time = 0




detector()
