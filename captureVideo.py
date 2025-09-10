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
import threading

exit1 = False
delayComparison = 0.2
photoMobile = None
photoFixed = None

def visibleComparison():
    global exit1, delayComparison, photoMobile, photoFixed, cv2
    
    print('...................inicio', flush = True)

    while not exit:
        if photoMobile is not None and photoFixed is not None:
            break
        time.sleep(delayComparison)
    return
    while not exit:
        cv2.imshow('union', photoMobile)
        cv2.waitKey(1)
        time.sleep(delayComparison)
        cv2.imshow('union', photoFixed)
        cv2.waitKey(1)
        time.sleep(delayComparison)
    '''
'''

p1 = threading.Thread(target=visibleComparison, args = ())
p1.daemon = True
p1.start()


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


status = globals.FIRST_FIXED_MIRROR
while True:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key):
        exit1 = True
        break
    photo = picam2.capture_array('raw')                 #photo have 16 bits when actually 8 bits where sent by the camera
    photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that    
    #resized_image = cv2.resize(photo, (RESIZED_WIDTH, RESIZED_HEIGHT)) 
    #resized_image = photo
    if globals.isBlackImage(photo):
        status = globals.BLACK_IMAGE
        #continue
    elif status == globals.BLACK_IMAGE:
        status = globals.FIRST_FIXED_MIRROR
    elif status == globals.FIRST_FIXED_MIRROR:
        status = globals.MOBILE_MIRROR
    elif status == globals.MOBILE_MIRROR:
        status = globals.SECOND_FIXED_MIRROR
        
    # if not status == globals.BLACK_IMAGE:
        # cv2.imshow('union', photo)
        # cv2.waitKey(1)
    if status == globals.MOBILE_MIRROR or status == globals.BLACK_IMAGE:
        cv2.imshow('mobile mirror', photo)
        cv2.waitKey(1)
    if status == globals.FIRST_FIXED_MIRROR or status == globals.SECOND_FIXED_MIRROR:
        photoFixed = photo
        cv2.imshow('fixed mirror', photo)
        cv2.waitKey(1)
        #status = globals.WAIT_BLACK_IMAGE
        
    if status == globals.MOBILE_MIRROR:
        photoMobile = photo
        
        #pub.publishImage(globals.FOTO_TAKEN_RESIZED, resized_image)    #resized for fast feedback
        #pub.publishImage(globals.FOTO_TAKEN, photo)                   #original for files


# When everything done, release the capture
picam2.stop()
#p1.join()
