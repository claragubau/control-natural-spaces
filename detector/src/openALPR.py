import time

import src.log as log_util
from openalpr import Alpr
from picamera import PiCamera

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
camera = PiCamera()
camera.start_preview()
previous = None
try:
    while True:
        time.sleep(5)
        camera.capture("/home/pi/latest.jpg")
        analysis = alpr.recognize_file("/home/pi/latest.jpg")
        if len(analysis["results"]):
            number_plate = analysis["results"][0]["plate"]
            if previous != number_plate:
               camera.stop_preview()
               log_util.info("Number plate detected: {}".format(number_plate))
               previous = number_plate

        # Wait for five seconds
        time.sleep(1)

except KeyboardInterrupt:
    log_util.info("Shutting down")
    alpr.unload()
