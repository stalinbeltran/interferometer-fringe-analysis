#python3 ./photoValidator.py
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2

pub = Publisher()
pub.init()
time.sleep(3)
print(pub)
pub.subscribe('phototaken')
time.sleep(3)

for message in pub.listen():
    value = message['data']
    if value == 'qc': exit()
    if isinstance(value, int) or len(value) < 200: continue
    imageBase64 = value
    img = pub.getImage(imageBase64)
    img = img.reshape((480, 640))
    # cv2.imshow('', img)
    # key = cv2.waitKey()
    break                               #debugging
    
