#python3 ./controller.py
import time
import numpy as np
from publisher import Publisher
import cv2 as cv2

pub = Publisher()
pub.init()
print(pub)
pub.subscribe('photovalidated')

for message in pub.listen():
    value = message['data']
    if value == 'qc': exit()
    if isinstance(value, int) or len(value) < 200: continue
    imageBase64 = value
    photo = pub.getImage(imageBase64, 640, 480)
    cv2.imshow('', photo)
    key = cv2.waitKey()
    break                               #debugging
    
cv2.destroyAllWindows()