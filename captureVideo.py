#python3 captureVideo.py

import numpy as np
import cv2 as cv
import imageSineFit as isf
from publisher import Publisher
import time
import redis

def init(hostIP = '127.0.0.1', port = 6379):
    redisdb = redis.Redis(
        host=hostIP,
        port=port,
        decode_responses=True # <-- this will ensure that binary data is decoded
    )
    return redisdb

redisdb = init()

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
pub = Publisher()
pub.init()
#time.sleep(3)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    photo = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    if not isf.isBlackImage(photo):
        pub.publishImage("phototaken", photo)       #publish photo
        #redisdb.publish("army-camp-1", 'message')
        cv.imshow('frame', photo)
    if cv.waitKey(1) == ord('q'):
        break
    break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()