import argparse
import time

import cv2
import numpy as np
import src.log as log_util
from openalpr import Alpr
from src.video_stream import VideoStream

parser = argparse.ArgumentParser()
parser.add_argument(
    "--resolution",
    help="Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.",
    default="1280x720",
)
parser.add_argument("--video", help="Path to the video, just for testing purposes", default=0)
args = parser.parse_args()

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

resW, resH = args.resolution.split("x")
imW, imH = int(resW), int(resH)

# Initialize video stream
video_stream = VideoStream(resolution=(imW, imH), video=args.video).start()
time.sleep(1.125)


def run():
    try:
        while True:
            # Grab frame from video stream
            frame1 = video_stream.read()
            # Acquire frame and resize to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            analysis = alpr.recognize_ndarray(frame)
            if len(analysis["results"]):
                number_plate = analysis["results"][0]["plate"]
                log_util.info("Number plate detected: {}".format(number_plate))
    except KeyboardInterrupt:
        log_util.info("Shutting down")
        alpr.unload()
        video_stream.stop()


if __name__ == "__main__":
    run()
