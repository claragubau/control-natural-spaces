import cv2
import time

import src.log as log_util
from openalpr import Alpr
from picamera import PiCamera
from picamera.array import PiRGBArray
from src.distance import levenshtein_distance
from src.request_utils import call_api

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
camera.start_preview()
previous = None
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        time.sleep(0.125)
        analysis = alpr.recognize_ndarray(frame)
        if len(analysis["results"]):
            number_plate = analysis["results"][0]["plate"]
            coordinates = [x for x in
                           [analysis["results"][0]["coordinates"][0]["x"],
                            analysis["results"][0]["coordinates"][0]["y"],
                            analysis["results"][0]["coordinates"][2]["x"],
                            analysis["results"][0]["coordinates"][2]["y"]]
                           ]
            if levenshtein_distance(previous, number_plate) > 2:
                log_util.info("Number plate detected: {}".format(number_plate))
                cv2.rectangle(frame, (int(coordinates[0]), int(coordinates[1])), (int(coordinates[2]), int(coordinates[3])), (0, 255, 0), 3)
                cv2.imwrite("/home/pi/latest.jpg", frame)
                response = call_api("/home/pi/latest.jpg", number_plate, coordinates)
                if response.status_code != 201:
                    log_util.info("License Plate was not sent properly")
                previous = number_plate

except KeyboardInterrupt:
    log_util.info("Shutting down")
    alpr.unload()
