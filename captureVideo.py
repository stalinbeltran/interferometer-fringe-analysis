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
RESIZED_WIDTH = globals.RESIZED_WIDTH
RESIZED_HEIGHT = globals.RESIZED_HEIGHT

config = picam2.create_video_configuration(
    raw = picam2.sensor_modes[0],
    buffer_count=12,
)
picam2.configure(config)
print(picam2.camera_configuration())
print(picam2.sensor_modes)
picam2.start()
picam2.set_controls({'ExposureTime':200})



factor = 0
offset = 0 #ns = 17us
smallAdjustment = 1700
baseOffset = 163000000
valid = False
c = 0
while True:
    # ~ key = globals.getKey()
    # ~ if globals.shouldCloseThisApp(key):
        # ~ valid = True
        # ~ print('q received')
    request = picam2.capture_request(flush = time.monotonic_ns() + baseOffset + factor * offset)
    photo = request.make_array('raw')                 #photo have 16 bits when actually 8 bits where sent by the camera
    request.release()
    photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that    
    #resized_image = cv2.resize(photo, (RESIZED_WIDTH, RESIZED_HEIGHT))
    # ~ cv2.imshow('', photo)
    # ~ cv2.waitKey(1)
    if not isf.isBlackImage(photo):
        c += 1
        if c > 2:
            valid = True
            print('valid')
        factor = 0
        cv2.imshow('sample', photo)
        cv2.waitKey(1)
        print('offset: ' + str(offset))
    elif valid:
        factor +=1
        offset +=smallAdjustment
        # ~ pub.publishImage(globals.FOTO_TAKEN_RESIZED, resized_image)    #resized for fast feedback
        # ~ pub.publishImage(globals.FOTO_TAKEN, photo)                   #original for files

# When everything done, release the capture
picam2.stop()
