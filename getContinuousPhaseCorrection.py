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
results = dataJSON
for key in results:
    previousSection = None
    if key == "hz": continue
    for result in results[key]:
        isContinuous = result["isContinuous"]
        section = result["section"]
        result["localPhaseCorrection"] = 0
        if not isContinuous or len(section) < 50: continue
        if previousSection:
            previousSectionAvg = sum(previousSection[-n:])/n
            sectionAvg = sum(section[:n])/n
            diff = previousSectionAvg-sectionAvg
            if abs(diff) > 0.5:
                if diff > 0: increment = 1
                else: increment = -1
                result["localPhaseCorrection"] = increment
                # print("previousSectionAvg: ", str(previousSectionAvg))
                # print("sectionAvg: ", str(sectionAvg))
                # exit(0)
        previousSection = section



outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)





