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
    resized_image = cv2.resize(photo, (320, 240))
    if not isf.isBlackImage(resized_image):
        pub.publishImage("phototakenresized", resized_image)    #resized for fast feedback
        pub.publishImage("phototaken", photo)                   #original for files

# When everything done, release the capture
picam2.stop()
