import time
import base64
import requests
from typing import List


def call_api(image_file: str, license_plate: str) -> dict:
    with open(image_file, "rb") as img_file:
        img_string = base64.b64encode(img_file.read()) 
    response = None
    for i in range(0, 5):
        try:
            response = requests.post(
                "http://192.168.0.15:5000/v1/detection",
                data={"image": img_string, "plate": license_plate},
            )
            assert response.status_code == 201
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


if __name__ == '__main__':
    call_api('./latest.jpg', 'TEST')
