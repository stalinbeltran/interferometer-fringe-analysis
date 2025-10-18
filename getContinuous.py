#python3 getContinuous.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseSoften.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-Continuous.json


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


MAXIMUM_DISTANCE = 0.03
MINIMUM_SECTION_LENGTH = 3
CONTINUOUS_FACTOR = 0.8
    

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
    if key == "hz": continue
    points = data[key]
    previousPoint = points[0]
    section = []
    continuousCounter = 0
    resultsKey = []
    previousIsContinuous = False
    for i in range(len(points)):
        point = points[i]
        distance = abs(previousPoint-point)
        thisIsContinuous = False
        if distance < MAXIMUM_DISTANCE:
            continuousCounter +=1
        else:
            actualSectionSize = len(section)
            if actualSectionSize > MINIMUM_SECTION_LENGTH:
                notContiguous = actualSectionSize - continuousCounter
                isContinuous = continuousCounter * CONTINUOUS_FACTOR > notContiguous
                saveSection(resultsKey, section, isContinuous)
                section = []
                previousIsContinuous = isContinuous
                continuousCounter = 0
        section.append(point)
        previousPoint = point
    actualSectionSize = len(section)
    isContinuous = actualSectionSize - continuousCounter > CONTINUOUS_FACTOR*actualSectionSize 
    saveSection(resultsKey, section, isContinuous)
    results[key] = resultsKey


outputJSON = results

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)



for key in results:
    begin = 0
    c = 0
    if key == "hz": continue
    for section in results[key]:
        isContinuous = section["isContinuous"]
        section = section["section"]
        if not isContinuous or len(section) < 50: continue
        end = begin + len(section)
        xdata = range(begin, end)
        ydata = section
        plt.plot(xdata, ydata, '.', label=key )
        begin = end
        c+=1
        if c % 8 == 0:
            plt.legend()
            plt.show()




