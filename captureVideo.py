#python3 captureVideo.py

import globals
import numpy as np
import cv2 as cv2
import imageSineFit as isf
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2

pub = Publisher()
pub.init()

picam2 = Picamera2()
WIDTH = globals.WIDTH
HEIGHT = globals.HEIGHT
config = picam2.create_video_configuration(raw = {'format': "SBGGR8", 'size': (HEIGHT, WIDTH)})
picam2.configure(config)
picam2.start()

while True:
    if globals.shouldCloseThisApp(): break
    photo = picam2.capture_array('raw')                 #photo have 16 bits when actually 8 bits where sent by the camera
    photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that
    if not isf.isBlackImage(photo):
        pub.publishImage("phototaken", photo)       #publish photo
    break

# When everything done, release the capture
picam2.stop()
