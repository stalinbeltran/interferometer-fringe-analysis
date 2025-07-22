#python3 captureVideo.py

import globals
import numpy as np
import cv2 as cv2
import imageSineFit as isf
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2

# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera for video capture
# You can adjust resolution, format, etc.
camera_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)

# Start the camera
picam2.start()


# cap = cv2.VideoCapture('/dev/video0')
# if not cap.isOpened():
    # print("Cannot open camera")
    # exit()
pub = Publisher()
pub.init()

key = None
while True:
    if globals.shouldCloseThisApp(): break
    # Capture frame-by-frame
    #ret, frame = cap.read()
    photo = picam2.capture_array()
    print('type(photo)')
    print(type(photo))
    print('shape')
    print(photo.shape)
    print(photo)
    # Display the resulting frame
    if not isf.isBlackImage(photo):
        pub.publishImage("phototaken", photo)       #publish photo
    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()