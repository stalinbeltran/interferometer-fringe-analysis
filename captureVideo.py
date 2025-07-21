#python3 captureVideo.py

import numpy as np
import cv2 as cv
import imageSineFit as isf
from publisher import Publisher
import time
import redis

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
pub = Publisher()
pub.init()

key = None
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    photo = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    print('type(photo)')
    print(type(photo))
    print('shape')
    print(photo.shape)
    print(photo)
    # Display the resulting frame
    if not isf.isBlackImage(photo):
        pub.publishImage("phototaken", photo)       #publish photo
        #cv.imshow('frame', photo)
        #key = cv.waitKey()
    if key == ord('c'):
        pub.publish("phototaken", 'qc')       
    if key == ord('q'):
        break
    break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()