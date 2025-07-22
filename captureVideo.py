#python3 captureVideo.py

import globals
import numpy as np
import cv2 as cv2
import imageSineFit as isf
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2

picam2 = Picamera2()
WIDTH = 1280
HEIGHT = 800
config = picam2.create_video_configuration(raw = {'format': "SBGGR8", 'size': (HEIGHT, WIDTH)})
picam2.configure(config)
picam2.start()


# yuv = picam2.capture_array('raw')
# grey = yuv[:HEIGHT, :WIDTH]

pub = Publisher()
pub.init()

key = None
while True:
    if globals.shouldCloseThisApp(): break
    # Capture frame-by-frame
    #ret, frame = cap.read()
    photo = picam2.capture_array('raw')
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
picam2.stop()
