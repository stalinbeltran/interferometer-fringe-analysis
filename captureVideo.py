#python3 captureVideo.py

import globals
import numpy as np
import cv2 as cv2
import imageSineFit as isf
from publisher import Publisher
import time
import redis
from picamera2 import Picamera2
from gpiozero import Button
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
picam2.set_controls({'ExposureTime':200})

c = 0
goodOnes= 0
lastOne = 0

def capture():
    global picam2, c, goodOnes
    lastOne = time.monotonic_ns()
    request = picam2.capture_request(flush = True) #6000
    photo = request.make_array('raw')                 #photo have 16 bits when actually 8 bits where sent by the camera
    request.release()
    photo = globals.toY8array(photo, WIDTH, HEIGHT)     #so we fix that
    # ~ cv2.imshow('sample', photo)
    # ~ cv2.waitKey(1)
    c +=1
    if c % 10 == 0:
        # ~ print('image' + str(c))
        print('goodOnes: ' + str(goodOnes))
        goodOnes = 0
    # ~ isf.isBlackImage(photo)
    if not isf.isBlackImage(photo):
        goodOnes +=1
        now = time.monotonic_ns()
        print('image: ' + str(c) + ' - elapsed: ' + str((now - lastOne)/1000))
        lastOne = now
        # ~ cv2.imshow('sample', photo)
        # ~ cv2.waitKey(1)
        # ~ pub.publishImage(globals.FOTO_TAKEN, photo)                   #original for files
        # ~ pub.publishImage(globals.FOTO_TAKEN_RESIZED, resized_image)    #resized for fast feedback

    key = globals.getKey()
    if globals.shouldCloseThisApp(key):
        picam2.stop()
        exit()
        # ~ valid = True
        # ~ print('q received')



button = Button(26)
button.when_pressed = capture

pause()
# When everything done, release the capture
picam2.stop()
