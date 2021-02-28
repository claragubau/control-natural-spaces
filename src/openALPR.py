
import time

import cv2
from openalpr import Alpr
from picamera import PiCamera
import src.log as log_util


alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtimedata")
camera = PiCamera()

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

try:
    while True:
        time.sleep(5)
        camera.capture('/home/pi/latest.jpg')
        analysis = alpr.recognize_file(
            "/home/pi/latest.jpg")
        if len(analysis['results']):
            number_plate = analysis['results'][0]['plate']
            log_util.info('Number plate detected: {}'.format(number_plate))
        # Wait for five seconds
        time.sleep(5)

except KeyboardInterrupt:
    log_util.info('Shutting down')
    alpr.unload()
    cv2.destroyAllWindows()

