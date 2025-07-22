#python3 ./photoValidator.py

import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2

pub = Publisher()
pub.init(hostIP='192.168.0.24')
print(pub)
pub.subscribe('phototaken')

while True:
    if globals.shouldCloseThisApp(): break
    message = pub.get_message()
    if message is None: continue
    value = message['data']
    if isinstance(value, int) or len(value) < 200: continue
    print('image')
    imageBase64 = value
    photo = pub.getImage(imageBase64, globals.WIDTH, globals.HEIGHT)
    pub.publishImage("photovalidated", photo)
    cv2.imshow('', photo)
    #key = cv2.waitKey()

    
cv2.destroyAllWindows()