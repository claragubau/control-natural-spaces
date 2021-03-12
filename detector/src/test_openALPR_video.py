import argparse
import time

import cv2
import numpy as np
import src.log as log_util
from openalpr import Alpr
from src.request_utils import call_api

parser = argparse.ArgumentParser()
parser.add_argument(
    "--resolution",
    help="Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.",
    default="1280x720",
)
parser.add_argument("--video", help="Path to the video, just for testing purposes", default=0)
args = parser.parse_args()

alpr = Alpr("eu", "/usr/local/share/openalpr/config/openalpr.defaults.conf", "openalpr/runtime_data/")

resW, resH = args.resolution.split("x")
imW, imH = int(resW), int(resH)

# Initialize video stream
video_stream = cv2.VideoCapture(args.video)

def run():
    try:
        while video_stream.isOpened():
            # Grab frame from video stream
            _, frame = video_stream.read()
            if frame is not None:
                # cv2.imshow("Image", frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #      break
                analysis = alpr.recognize_ndarray(frame)
                if len(analysis["results"]):
                    number_plate = analysis["results"][0]["plate"]
                    cv2.imwrite("./latest.jpg", frame)
                    response = call_api("./latest.jpg", number_plate)
                    print(response)
        video_stream.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print('Exception happened: {}'.format(e))

if __name__ == "__main__":
    run()
