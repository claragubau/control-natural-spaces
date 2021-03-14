import argparse

import cv2
import time
import numpy as np
from openalpr import Alpr
from src.request_utils import call_api

parser = argparse.ArgumentParser()
parser.add_argument("--video", help="Path to the video, just for testing purposes", default=0)
args = parser.parse_args()

alpr = Alpr("eu", "/usr/local/share/openalpr/config/openalpr.defaults.conf", "openalpr/runtime_data/")

# Initialize video stream
video_stream = cv2.VideoCapture(args.video)
frame_rate = 30


def run():
    try:
        prev = 0
        while True:
            time_elapsed = time.time() - prev
            if time_elapsed > 1. / frame_rate:
                _, frame = video_stream.read()
                prev = time.time()
                analysis = alpr.recognize_ndarray(frame)
                if len(analysis["results"]):
                    number_plate = analysis["results"][0]["plate"]
                    coordinates = [x for x in
                                   [analysis["results"][0]["coordinates"][0]["x"],
                                    analysis["results"][0]["coordinates"][0]["y"],
                                    analysis["results"][0]["coordinates"][2]["x"],
                                    analysis["results"][0]["coordinates"][2]["y"]]
                                   ]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 3
                    (text_width, text_height) = cv2.getTextSize(number_plate, font, fontScale=font_scale, thickness=1)[0]
                    box_coords = ((coordinates[2], coordinates[3]), (coordinates[2] + text_width + 2, coordinates[3] - text_height - 2))
                    cv2.rectangle(frame, box_coords[0], box_coords[1], (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, number_plate, (coordinates[2], coordinates[3]), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (240, 0, 0), 3)
                    frame_resized = cv2.resize(frame, (720, 480))
                    cv2.imshow("Test", frame)
                    cv2.waitKey(10000)
                    #cv2.imwrite("./latest_{}.jpg".format(time_elapsed), frame)
                    #response = call_api("./latest.jpg", number_plate)
                    #print(response)
        video_stream.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print('Exception happened: {}'.format(e))


if __name__ == "__main__":
    run()
