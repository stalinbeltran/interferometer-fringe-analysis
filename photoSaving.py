#python3 ./photoValidator.py

import globals
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2
import imageSineFit as isf


filename = sys.argv[1]

def saveFile(filepath, data):
    with open(filepath, 'wb') as file:
        file.write(data)


pub = Publisher()
pub.init(hostIP='localhost')
print(pub)
pub.subscribe(globals.FOTO_TAKEN)      #subscribe for the resized version only (it is faster than original)

c=0
while True:
    key = globals.getKey()
    if globals.shouldCloseThisApp(key): break
    message = pub.get_message()
    if message is None: continue
    timestamp = time.datetime.now()
    filepath = filename + '-' + timestamp + '-' + '.png'
    imageBase64 = message['data']
    photo = pub.getImage(imageBase64, globals.WIDTH, globals.HEIGHT)         #globals.WIDTH, globals.HEIGHT)
    saveFile(filepath, photo)
    # ~ resized_image = cv2.resize(photo, (2*globals.RESIZED_WIDTH, 2*globals.RESIZED_HEIGHT))
    cv2.imshow('photoValidator', photo)
    cv2.waitKey(1)

cv2.destroyAllWindows()
