import time

import src.log as log_util
from src.request_utils import call_api
from openalpr import Alpr
from picamera import PiCamera

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
camera = PiCamera()
camera.start_preview()
previous = None
try:
    while True:
        time.sleep(0.125)
        camera.capture("/home/pi/latest.jpg")
        analysis = alpr.recognize_file("/home/pi/latest.jpg")
        if len(analysis["results"]):
            number_plate = analysis["results"][0]["plate"]
            if previous != number_plate:
               camera.stop_preview()
               log_util.info("Number plate detected: {}".format(number_plate))
               response = call_api("/home/pi/latest.jpg", number_plate)
               if response.status_code != 201:
                   log_util.info("License Plate was not sent properly")
               previous = number_plate

except KeyboardInterrupt:
    log_util.info("Shutting down")
    alpr.unload()
