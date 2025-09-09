#python3 captureVideo.py

import globals
import numpy as np
import cv2 as cv2
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2
from gpiozero import Button, DigitalInputDevice
from signal import pause


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
#picam2.set_controls({'ExposureTime':200})


status = globals.FIRST_FIXED_MIRROR
while True:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key): break
    photo = picam2.capture_array('raw')                 #photo have 16 bits when actually 8 bits where sent by the camera
    photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that    
    #resized_image = cv2.resize(photo, (RESIZED_WIDTH, RESIZED_HEIGHT)) 
    #resized_image = photo
    if globals.isBlackImage(photo):
        status = globals.BLACK_IMAGE
        continue
    elif status == globals.BLACK_IMAGE:
        status = globals.FIRST_FIXED_MIRROR
    elif status == globals.FIRST_FIXED_MIRROR:
        status = globals.MOBILE_MIRROR
    elif status == globals.MOBILE_MIRROR:
        status = globals.SECOND_FIXED_MIRROR
        
    if status == globals.MOBILE_MIRROR:
        cv2.imshow('mobile mirror', photo)
        cv2.waitKey(1)
    if status == globals.SECOND_FIXED_MIRROR:
        cv2.imshow('fixed mirror', photo)
        cv2.waitKey(1)
        status = globals.WAIT_BLACK_IMAGE
        
        #pub.publishImage(globals.FOTO_TAKEN_RESIZED, resized_image)    #resized for fast feedback
        #pub.publishImage(globals.FOTO_TAKEN, photo)                   #original for files


# When everything done, release the capture
picam2.stop()
