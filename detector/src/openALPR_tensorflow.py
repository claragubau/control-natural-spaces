import argparse
import importlib.util
import time

import cv2
import numpy as np
import src.log as log_util
from openalpr import Alpr
from src.video_stream import VideoStream

parser = argparse.ArgumentParser()
parser.add_argument(
    "--graph", help="Path of the .tflite file, if different than detect.tflite", default="detect.tflite"
)
parser.add_argument(
    "--labels", help="Path of the labelmap file, if different than labelmap.txt", default="labelmap.txt"
)
parser.add_argument("--threshold", help="Minimum confidence threshold for displaying detected objects", default=0.5)
parser.add_argument("--mode", help="0 is Camera Mode, 1 is Image mode, 2 is Video Mode")
parser.add_argument(
    "--resolution",
    help="Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.",
    default="1280x720",
)
args = parser.parse_args()

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtimedata")

pkg = importlib.util.find_spec("tflite_runtime")
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter


min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split("x")
imW, imH = int(resW), int(resH)


# Load the label map
with open(args.labels) as f:
    labels = [line.strip() for line in f.readlines()]

# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=args.graph)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]["shape"][1]
width = input_details[0]["shape"][2]

floating_model = input_details[0]["dtype"] == np.float32

input_mean = 127.5
input_std = 127.5

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
video_stream = VideoStream(resolution=(imW, imH)).start()
time.sleep(1)


def run(threshold):
    try:
        while True:
            time.sleep(5)
            # Grab frame from video stream
            frame1 = video_stream.read()

            # Acquire frame and resize to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)

            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]["index"], input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[0]["index"])[
                0
            ]  # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]["index"])[0]  # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]["index"])[0]  # Confidence of detected objects

            # Loop over all detections and draw detection box if confidence is above minimum threshold
            for i in range(len(scores)):
                if ((scores[i] > threshold) and (scores[i] <= 1.0)) and labels[int(classes[i])] == "car":
                    log_util.info("A Car was detected")
                    # TODO: check if alpr can work with a numpy array
                    analysis = alpr.recognize_file()
                    if len(analysis["results"]):
                        number_plate = analysis["results"][0]["plate"]
                        log_util.info("Number plate detected: {}".format(number_plate))
    except KeyboardInterrupt:
        log_util.info("Shutting down")
        alpr.unload()
        cv2.destroyAllWindows()
        video_stream.stop()


if __name__ == "__main__":
    run(args.threshold)
