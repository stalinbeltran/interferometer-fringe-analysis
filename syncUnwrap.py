#python3 syncUnwrap.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-unwrapped.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PlainData.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-unwrapped2.json fixedPhase mobilePhase

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
input_file_original = (sys.argv[2])
output_file = (sys.argv[3])
unwrappedKey = (sys.argv[4])
wrappedKey = (sys.argv[5])


def syncUnwrap(unwrappedData, unwrappedDataOriginal, wrappedData):
    size = len(unwrappedData)
    wrappedDataUnwrapped = []
    for i in range(size):
        distance = unwrappedData[i] - unwrappedDataOriginal[i]
        distanceInt = int(distance)
        wrappedDataUnwrapped.append(wrappedData[i] + distanceInt)
        
    return wrappedDataUnwrapped


with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)


with open(input_file_original, 'r', encoding='utf-8') as f:
    dataOriginal = json.load(f)
    
    

wrappedData = (data[0]["data"][wrappedKey])
unwrappedData = (data[0]["data"][unwrappedKey])
unwrappedDataOriginal = (dataOriginal[0]["data"][unwrappedKey])

wrappedDataUnwrapped = syncUnwrap(unwrappedData, unwrappedDataOriginal, wrappedData)
data[0]["data"][wrappedKey] = wrappedDataUnwrapped
print("end")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ended")
