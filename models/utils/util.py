import os
import string

import cv2
import easyocr
import mysql.connector
import datetime

from google.cloud import vision

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                        'license_plate' in results[frame_nmr][car_id].keys() and \
                        results[frame_nmr][car_id]['license_plate']['text'] is not None:
                    print("INSIDE IF BLOCK")
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()


# def license_complies_format(text):
#     """
#     Check if the license plate text complies with the required format.
#
#     Args:
#         text (str): License plate text.
#
#     Returns:
#         bool: True if the license plate complies with the format, False otherwise.
#     """
#
#     if len(text) == 6:
#         if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
#                 (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
#                 (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                     2] in dict_char_to_int.keys()) and \
#                 (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                     3] in dict_char_to_int.keys()) and \
#                 (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                     4] in dict_char_to_int.keys()) and \
#                 (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[5] in dict_char_to_int.keys()):
#             return True
#         else:
#             return False
#     else:
#         if len(text) == 7:
#             if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
#                     (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
#                     (text[2] in string.ascii_uppercase or text[2] in dict_int_to_char.keys()) and \
#                     (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                         3] in dict_char_to_int.keys()) and \
#                     (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                         4] in dict_char_to_int.keys()) and \
#                     (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                         5] in dict_char_to_int.keys()) and \
#                     (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[
#                         6] in dict_char_to_int.keys()):
#                 return True
#             else:
#                 return False


import string


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.
    License plate can either start with 2 or 3 uppercase letters followed by 4 digits.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """

    # Remove all spaces from the text
    text = text.replace(" ", "")

    # Check if length matches either 6 or 7 characters
    if len(text) == 6:
        # Format: 2 uppercase letters followed by 4 digits (e.g., AE2342)
        if text[:2].isalpha() and text[:2].isupper() and text[2:].isdigit():
            return True

    elif len(text) == 7:
        # Format: 3 uppercase letters followed by 4 digits (e.g., CAE9132)
        if text[:3].isalpha() and text[:3].isupper() and text[3:].isdigit():
            return True

    # If none of the conditions match, return False
    return False


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    if len(text) == 6:

        mapping = {0: dict_int_to_char, 1: dict_int_to_char,2: dict_char_to_int,3: dict_char_to_int, 4: dict_char_to_int, 5: dict_char_to_int}
        for j in [0, 1, 2, 3, 4, 5]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]

        return license_plate_
    else :
        mapping = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_int_to_char, 3: dict_char_to_int,
                   4: dict_char_to_int, 5: dict_char_to_int,6: dict_char_to_int}
        for j in [0, 1, 2, 3, 4, 5,6]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]

        return license_plate_




def extract_the_text_from_CV2image(cv2_image):
    """
          Use Google vision api to read text from given image

          returns
            text

           """

    # Use environment variable for credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Wicky\Documents\GitHub\group_project_code\credentials\avid-circle-432005-d6-500c180b6ddf.json"

    client = vision.ImageAnnotatorClient()

    # Here converting cv2 image in to jpg because cloud vision do not support cv2 format
    success, encoded_image = cv2.imencode('.jpg', cv2_image)
    content = encoded_image.tobytes()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    text = ""

    for text in texts:
        description = text.description
        text = description
        break

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


    print(f"Licence plate text = {text}***************************************************************************")
    return text


# def read_license_plate(license_plate_crop):
#     """
#     Read the license plate text from the given cropped image.
#
#     Args:
#         license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.
#
#     Returns:
#         tuple: Tuple containing the formatted license plate text and its confidence score.
#     """
#
#     # detections = reader.readtext(license_plate_crop)
#
#     # for detection in detections:
#     #     bbox, text, score = detection
#     #     filtered_text = ''.join(char for char in text if char.isalnum())
#     #     #debug code
#     #     with open(r"C:\Users\Wicky\Documents\GitHub\group_project_code\Client\public\raw_number_plate", "a") as file_object:
#     #         text_to_append = f"{filtered_text}\n"
#     #         file_object.write(text_to_append)
#
#         # text = text.upper().replace(' ', '')
#         # debugCode
#     filtered_text = extract_the_text_from_CV2image(license_plate_crop)
#     score = 0
#
#         if license_complies_format(filtered_text):
#             finalize_number_plate =  format_license(filtered_text), score
#
#             #debug
#
#             current_datetime = datetime.datetime.now()
#             current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
#             changes = "add adaptive thresh block size:21 c:30"
#
#
#             with open(r"C:\Users\Wicky\Documents\GitHub\group_project_code\Client\public\final_number_plates", "a") as file_object:
#                 text_to_append = f"number_plate = {filtered_text} confidence_score = {score} changes = {changes} date&time = {current_datetime_str}\n"
#                 file_object.write(text_to_append)
#             return finalize_number_plate
#
#     return None, None


import datetime


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    # Assuming `extract_the_text_from_CV2image` and `license_complies_format` are defined elsewhere
    filtered_text = extract_the_text_from_CV2image(license_plate_crop)
    score = 0  # Placeholder for confidence score. Update with actual confidence calculation.
    print(f"Licence plate text = {filtered_text} license_complies_format = {license_complies_format(filtered_text)}  ****************************")
    if license_complies_format(filtered_text):
        # finalize_number_plate = format_license(filtered_text), score
        finalize_number_plate = filtered_text
        # Debugging and logging information
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        changes = "add adaptive thresh block size:21 c:30"

        with open(r"C:\Users\Wicky\Documents\GitHub\group_project_code\Client\public\final_number_plates",
                  "a") as file_object:
            text_to_append = (f"number_plate = {filtered_text} confidence_score = {score} "
                              f"changes = {changes} date&time = {current_datetime_str}\n")
            file_object.write(text_to_append)

        return finalize_number_plate,score

    return None, None


def get_vehicle_type(class_id):
    if class_id == 2:
        return "Car"
    elif class_id == 3:
        return "Motorcycle"
    elif class_id == 5:
        return "Bus"  # Assuming 5 corresponds to a bus
    elif class_id == 7:
        return "Truck"
    else:
        return "Other"  # For any other class IDs

def insert_data_to_data_base(database, table_name, number_plate_text, in_or_out, image_url,socketio,vehicle_id):
    current_datetime = datetime.datetime.now()
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_date = current_datetime.day
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute
    current_second = current_datetime.second
    vehicle_type = get_vehicle_type(vehicle_id)

    print(f"***************************************vehicle id = {vehicle_type}")

    host = "localhost"
    user = "root"
    password = ""
    database = database

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()
    sql = (f"INSERT INTO {table_name} (year, month, date, hour, minute, second, number_plate, image_url, in_or_out,vehicle_type) "
           f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)")
    data = (current_year, current_month, current_date, current_hour, current_minute, current_second, number_plate_text,
            image_url, in_or_out,vehicle_type)

    cursor.execute(sql, data)
    connection.commit()

    cursor.close()
    connection.close()

    # Emit the new entry to the frontend via WebSocket
    new_entry = {
        'date': f"{current_year}/{str(current_month).zfill(2)}/{str(current_date).zfill(2)}",
        'time': f"{str(current_hour).zfill(2)}:{str(current_minute).zfill(2)}:{str(current_second).zfill(2)}",
        'numberPlate': number_plate_text,
        'vehicleType': 'other',  # Default to 'other' since we don't have this info
        'status': in_or_out,
        'image_url': image_url,
        'vehicle_type':vehicle_type
    }

    # Emit the new data through socket to connected clients
    socketio.emit('new_entry', new_entry)
