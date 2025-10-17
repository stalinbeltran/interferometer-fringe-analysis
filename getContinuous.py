#python3 getContinuous.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseSoften.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-Continuous.json


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
#parameters = (sys.argv[3])


MAXIMUM_DISTANCE = 0.01
    

def saveSection(results, section, isContinuous):
    if len(section) == 0:            #we have nothing to save
        return
    result = {"isContinuous" : isContinuous, "section" : section}
    results.append(result)

    

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)


data = dataJSON[1]["data"]          #take the softened data
results = {}
for key in data:
    points = data[key]
    previousPoint = points[0]
    section = []
    isContinuous = True
    resultsKey = []
    for i in range(len(points)):
        point = points[i]
        distance = abs(previousPoint-point)
        thisIsContinuous = False
        if distance < MAXIMUM_DISTANCE:
            thisIsContinuous = True
        if thisIsContinuous != isContinuous:
            saveSection(resultsKey, section, isContinuous)
            section = []
            isContinuous = thisIsContinuous
        section.append(point)
        previousPoint = point
    saveSection(resultsKey, section, isContinuous)
    results[key] = resultsKey
    


outputJSON = results

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)





