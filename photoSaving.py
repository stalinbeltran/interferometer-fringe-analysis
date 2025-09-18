#python photoSaving.py ./Videos/monday15092025/fringes_15092025

import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2
import sys


filename = sys.argv[1]

def saveFile(filepath, img):
    cv2.imwrite(filepath, img)


pub = Publisher()
pub.init(hostIP='localhost')
print(pub)
pub.subscribe(globals.FOTO_TAKEN)      #subscribe for the resized version only (it is faster than original)

c=0
while True and c<10:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key): break
    message = pub.get_message()
    if message is None: continue
    timestamp = time.time()
    filepath = filename + '-' + str(timestamp) + '-' + '.png'
    imageBase64 = message['data']
    if type(imageBase64) == int: continue
    photo = pub.getImage(imageBase64, globals.WIDTH, globals.HEIGHT)         #globals.WIDTH, globals.HEIGHT)
    saveFile(filepath, photo)
    c+=1
    # ~ resized_image = cv2.resize(photo, (2*globals.RESIZED_WIDTH, 2*globals.RESIZED_HEIGHT))
    # cv2.imshow('photoSaving', photo)
    # cv2.waitKey(1)

cv2.destroyAllWindows()
