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


MAXIMUM_DISTANCE = 0.09
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
hz = data["hz"]
deltaPhase = data["deltaPhase"]
print(len(deltaPhase))


previousPoint = deltaPhase[0]
section = {"deltaPhase":[], "hz":[]}
continuousCounter = 0
results = []
previousIsContinuous = False
for i in range(len(deltaPhase)):
    point = deltaPhase[i]
    distance = abs(previousPoint-point)
    thisIsContinuous = False
    if distance < MAXIMUM_DISTANCE:             #distance between contiguous poinnts signal continuity
        continuousCounter +=1
    else:
        actualSectionSize = len(section["deltaPhase"])
        if actualSectionSize > MINIMUM_SECTION_LENGTH:
            notContiguous = actualSectionSize - continuousCounter
            isContinuous = continuousCounter * CONTINUOUS_FACTOR > notContiguous
            saveSection(results, section, isContinuous)
            section = {"deltaPhase":[], "hz":[]}
            previousIsContinuous = isContinuous
            continuousCounter = 0
    section["deltaPhase"].append(deltaPhase[i])
    section["hz"].append(hz[i])
    previousPoint = point
actualSectionSize = len(section["deltaPhase"])
isContinuous = actualSectionSize - continuousCounter > CONTINUOUS_FACTOR*actualSectionSize 
saveSection(results, section, isContinuous)




outputJSON = results

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)



begin = 0
c = 0
for section in results:
    isContinuous = section["isContinuous"]
    section = section["section"]
    end = begin + len(section["deltaPhase"])
    xdata = range(begin, end)
    ydata = section["deltaPhase"]
    marker = '.'
    if isContinuous: marker = '-'
    plt.plot(xdata, ydata, marker)
    begin = end
    c+=1
    if c % 50 == 0:
        plt.show()

plt.show()


