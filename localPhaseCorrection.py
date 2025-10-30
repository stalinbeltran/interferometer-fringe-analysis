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
ykey = (sys.argv[4])
ykey = ykey.split(':')
phaseMaxDifference = float(sys.argv[5])
distanceImprovementFactor = float(sys.argv[6])
N_lastPoints = int(sys.argv[7])
iterations = int(sys.argv[8])


def correctLocalPhaseByReference(data, referenceData):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    processed = 0
    points = data
    size = len(points)
    for index in range(size):
        phase = points[index]
        newphase = phase
        aroundPoints = globals.getAroundPoints2(index, N_lastPoints, referenceData)
        averageSamplePhase = globals.pointsAverage(aroundPoints)
        distance = abs(averageSamplePhase-phase)
        increment = round(distance)                                            #only increment/decrement an integer number of times, to keep phase information
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
for i in range(iterations):
    for key in ykey:
        correctLocalPhaseByReference(data[0]["data"][key], referenceData)
        print()


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ended")
