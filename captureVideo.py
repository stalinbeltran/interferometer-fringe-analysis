#python3 captureVideo.py

import globals
import numpy as np
import cv2 as cv2
import imageSineFit as isf
from publisher import Publisher
import time
import redis

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
pub = Publisher()
pub.init()

key = None
c = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    photo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print('type(photo)')
    print(type(photo))
    print('shape')
    print(photo.shape)
    print(photo)
    # Display the resulting frame
    if not isf.isBlackImage(photo):
        pub.publishImage("phototaken", photo)       #publish photo
        #cv2.imshow('frame', photo)
        #key = cv2.waitKey()
        c +=1
    if key == ord('c'):
        pub.publish("phototaken", 'qc')       
    if key == ord('q'):
        break

    if c == 2: break                               #debugging
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()