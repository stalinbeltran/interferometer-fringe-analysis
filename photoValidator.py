#python3 ./photoValidator.py

import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2
import imageSineFit as isf

guessedWavelength = 350
pub = Publisher()
pub.init(hostIP='192.168.0.24')
print(pub)
pub.subscribe('phototaken')

c=0
while True:
    if globals.shouldCloseThisApp(): break
    message = pub.get_message()
    if message is None: continue
    value = message['data']
    if isinstance(value, int) or len(value) < 200: continue
    c +=1
    if c % 10 == 0: print('image' + str(c))
    imageBase64 = value
    photo = pub.getImage(imageBase64, globals.WIDTH, globals.HEIGHT)
    photoHorizontalMean = isf.getHorizontalMean(photo)
    fitData = isf.verticalSineFit(photoHorizontalMean, guessedWavelength)
    print(2*np.pi/fitData["frequency"]["value"])
    pub.publishImage("photovalidated", photo)
    cv2.imshow('', photoHorizontalMean)
    cv2.waitKey(1)

    
cv2.destroyAllWindows()