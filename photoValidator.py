#python3 ./photoValidator.py

import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2

pub = Publisher()
pub.init()
print(pub)
pub.subscribe('phototaken')

c = 0
while True:
    if globals.shouldCloseThisApp(): break
    message = pub.get_message()
    if message is None: continue
    value = message['data']
    if value == 'qc': exit()
    if isinstance(value, int) or len(value) < 200: continue
    imageBase64 = value
    photo = pub.getImage(imageBase64, 640, 480)
    pub.publishImage("photovalidated", photo)
    # cv2.imshow('', photo)
    # key = cv2.waitKey()
    c +=1
    if c == 2: break                               #debugging
    
cv2.destroyAllWindows()