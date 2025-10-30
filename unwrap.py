#python3 unwrap.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PlainData.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-unwrapped.json 

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
ykey = (sys.argv[3])
ykey = ykey.split(':')


def unwrap(data):
    normalizedData = [x*2*np.pi for x in data]
    unwrappedData = np.unwrap(normalizedData)
    normalizedData = [x/(2*np.pi) for x in unwrappedData]
    normalizedData = normalizedData
    return normalizedData


with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
for key in ykey:
    unwrappedData = unwrap(data[0]["data"][key])
    data[0]["data"][key] = unwrappedData
    print()


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ended")
