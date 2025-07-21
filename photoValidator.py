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
    print(type(value))
    if isinstance(value, int) or len(value) < 200: continue
    imageBase64 = value
    img = pub.getImage(imageBase64)
    print(type(img))
    img = img.reshape((480, 640))
    print('shape')
    print(img.shape)
    print(img)
    cv2.imshow('', img)
    key = cv2.waitKey()
    break
    
