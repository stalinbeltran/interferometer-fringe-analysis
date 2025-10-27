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


sections = dataJSON
previousData = None
absolutePhaseCorrection = 0
for section in sections:
    isContinuous = section["isContinuous"]
    if not isContinuous: continue
    size = section["size"]
    data = section["data"]["softened"]["deltaPhase"]
    section["localPhaseCorrection"] = 0
    if previousData:
        previousDataAvg = sum(previousData)/len(previousData)
        dataAvg = sum(data)/len(data)
        diff = previousDataAvg-dataAvg
        increment = int(diff)
        absolutePhaseCorrection += increment
        section["localPhaseCorrection"] = increment
        section["absolutePhaseCorrection"] = absolutePhaseCorrection
        # print("previousDataAvg: ", str(previousDataAvg))
        # print("dataAvg: ", str(dataAvg))
        # exit(0)
    previousData = data



outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)





