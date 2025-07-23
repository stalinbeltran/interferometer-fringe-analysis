#python3 ./photoValidator.py

import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2
import imageSineFit as isf



pub = Publisher()
pub.init(hostIP='localhost')
print(pub)
pub.subscribe(globals.FOTO_TAKEN_RESIZED)      #subscribe for the resized version only (it is faster than original)

c=0
while True:
    if globals.shouldCloseThisApp(): break
    message = pub.get_message()
    if message is None: continue
    value = message['data']
    if isinstance(value, int): continue
    c +=1
    if c % 10 == 0: print('image' + str(c))
    imageBase64 = value
    photo = pub.getImage(imageBase64, globals.RESIZED_WIDTH, globals.RESIZED_HEIGHT)         #globals.WIDTH, globals.HEIGHT)
    resized_image = cv2.resize(photo, (2*globals.RESIZED_WIDTH, 2*globals.RESIZED_HEIGHT))
    cv2.imshow('', resized_image)
    cv2.waitKey(1)
    if globals.shouldPauseThisApp():
        print('listos para pausarla')
        pub.unsubscribe(globals.FOTO_TAKEN_RESIZED)        #to avoid being disconnected while waiting
        cv2.waitKey()      #the idea is to keep that last image visible, for comparison
        pub.subscribe(globals.FOTO_TAKEN_RESIZED)
cv2.destroyAllWindows()
