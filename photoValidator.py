#python3 ./photoValidator.py
import time
import numpy as np
from publisher import Publisher

pub = Publisher()
pub.init()
time.sleep(3)
print(pub)
pub.subscribe('phototaken')
time.sleep(3)

for message in pub.listen():
    print((message))
    value = message['data']
    if value == 'qc': exit()
    print(type(value))
    if isinstance(value, int) or len(value) < 200: continue
    imageBase64 = value
    img = pub.getImage(imageBase64)
    print(type(img))
    
