#python3 normalizeSections.py


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

input_file = (sys.argv[1])
output_file = (sys.argv[2])


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

accumulatedIncrement = 0
for section in dataJSON:
    isContinuous = section["isContinuous"]
    if not isContinuous: continue               #ignore discontinuities
    increment = section["localPhaseCorrection"]
    accumulatedIncrement += increment
    data = section["data"]
    for key in data:
        datakey = data[key]["deltaPhase"]
        size = len(datakey)
        for i in range(size):
            datakey[i] = datakey[i] + accumulatedIncrement
    

outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

