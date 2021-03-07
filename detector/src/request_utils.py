import os
import time
import base64
import requests


def call_api(image_file:str, license_plate:str):
    with open(image_file, "rb") as img_file:
        img_string = base64.urlsafe_b64encode(img_file.read())
    response = None
    for i in range(0, 5):
        try:
            response = requests.post(
                "https://localhost:5000/v1/detection",
                data={"image": img_string, "license_plate": license_plate},
            )
            assert resonse.status_code == 201
            response_dict = response.json()
            return response_dict
        except Exception as e:
            if i < 2:
                time.sleep(0.125)
            else:
                print(
                    "Image failed, throwing error! [{}] - [{}]".format(
                        e, "None" if not response else response.status_code
                    )
                )
                print("Image that failed:{}".format(image_file))
                return [], []