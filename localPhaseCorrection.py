#python3 localPhaseCorrection.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PlainData.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-LocalPhaseCorrected.json 

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
timestampRange = globals.getPromptOptionalParameter(8, [{"func":globals.split, "funcParams":[":"]}, {"func":float}])




def correctLocalPhaseByReference(data, referenceData):
    global distanceImprovementFactor, N_lastPoints, timestampData, timestampRange
    processed = 0
    points = data
    size = len(points)
    c = 0
    if timestampRange:
        timestampStart = timestampRange[0]
        timestampEnd = timestampRange[1]
    for index in range(size):
        if timestampRange:                              #custom range processing
            thisTimestamp = timestampData[index]
            if thisTimestamp < timestampStart: continue
            if thisTimestamp > timestampEnd: continue
        phase = points[index]
        newphase = phase
        aroundPoints = globals.getAroundPoints2(index, N_lastPoints, referenceData)
        averageSamplePhase = globals.pointsAverage(aroundPoints)
        distance = abs(averageSamplePhase-phase)
        if c < 20:
            print("averageSamplePhase: ", averageSamplePhase)
            print("distance: ", distance)
        c+=1
        increment = round(distance)                                            #only increment/decrement an integer number of times, to keep phase information
        if increment == 0: increment = 1
        increasedPhaseDistance = abs(averageSamplePhase-(phase + (increment)))
        decreasedPhaseDistance = abs(averageSamplePhase-(phase - (increment)))
        if increasedPhaseDistance < distance*distanceImprovementFactor:
            newphase = phase+increment          #if we can make it closer to average, we do
            processed+=1
        elif decreasedPhaseDistance < distance*distanceImprovementFactor:
            newphase = phase-increment
            processed+=1
        points[index] = newphase

    print("processed: ", processed)
    return processed


with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

referenceData = data[0]["data"][referenceKey]
timestampData = data[0]["data"]["timestamp"]
for i in range(iterations):
    for key in ykey:
        correctLocalPhaseByReference(data[0]["data"][key], referenceData)
        print()


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ended")
