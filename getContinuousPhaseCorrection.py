#python3 getContinuousPhaseCorrection.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-Continuous.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseCorrection.json 


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
output_file = (sys.argv[2])
#parameters = (sys.argv[3])


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

n = 10
sections = dataJSON
previousData = None
for section in sections:
    coef = section["regression"]["coef"]
    size = section["size"]
    isContinuous = section["isContinuous"]
    if size < 51: isContinuous = False      #discard too short sections
    section["isContinuous"] = isContinuous
    data = section["data"]["softened"]["deltaPhase"]
    section["localPhaseCorrection"] = 0
    if not isContinuous: continue
    if previousData:
        previousDataAvg = sum(previousData[-n:])/n
        dataAvg = sum(data[:n])/n
        diff = previousDataAvg-dataAvg
        increment = int(diff)
        section["localPhaseCorrection"] = increment
        # print("previousDataAvg: ", str(previousDataAvg))
        # print("dataAvg: ", str(dataAvg))
        # exit(0)
    previousData = data



outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)





