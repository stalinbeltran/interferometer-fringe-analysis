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

for section in dataJSON:
    isContinuous = section["isContinuous"]
    if not isContinuous: continue               #ignore discontinuities
    data = section["data"]
    size = section["size"]
    if size < 10: continue
    ydata = data["original"]["deltaPhase"]
    minimum = min(ydata)
    for i in range(size):
        ydata[i] = ydata[i] - minimum
    

outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

