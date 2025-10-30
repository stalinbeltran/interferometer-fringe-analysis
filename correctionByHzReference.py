#python3 

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
referenceKey = (sys.argv[3])
ykey = globals.getPromptOptionalParameter(4, [{"func":globals.split, "funcParams":[":"]}])
distanceImprovementFactor = float(sys.argv[5])
N_lastPoints = int(sys.argv[6])
iterations = int(sys.argv[7])
positionRange = globals.getPromptOptionalParameter(8, [{"func":globals.split, "funcParams":[":"]}, {"func":float}])




def correctLocalPhaseByReference(data, referenceData):
    global distanceImprovementFactor, N_lastPoints, timestampData, positionRange
    processed = 0
    points = data
    size = len(points)
    c = 0
    if positionRange:
        start = positionRange[0]
        end = positionRange[1]
    for index in range(size):
        if positionRange:                              #custom range processing
            if index < start: continue
            if index > end: continue
        phase = points[index]
        newphase = phase
        aroundPoints = globals.getAroundPoints2(index, N_lastPoints, referenceData)
        averageSamplePhase = globals.pointsAverage(aroundPoints)
        distance = (averageSamplePhase-phase)
        if c < 20:
            print("averageSamplePhase: ", averageSamplePhase)
            print("distance: ", distance)
        c+=1
        increment = 0                                            #zero increment by default
        if distance > 0: increment = 1                           #increment if below the reference signal only
        newphase += increment
        points[index] = newphase
        processed+=1

    print("processed: ", processed)
    return processed


with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

referenceData = data[0]["data"][referenceKey]
for i in range(iterations):
    for key in ykey:
        correctLocalPhaseByReference(data[0]["data"][key], referenceData)
        print()


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ended")
