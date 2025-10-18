#python3 signalSynchronizer.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseUnwraped.json  D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-Sync.json  

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = float(sys.argv[3])             #0.7    #max allowed diff between average and a point
N_lastPoints = int(sys.argv[4])                     #40
distanceImprovementFactor = 0.9


def sync(dataJSON, phaseKeyReference, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    dataReference = dataJSON[0]["data"][phaseKeyReference]
    data = dataJSON[0]["data"][phaseKey]
    processed = 0
    show = False
    showed = 0
    maxShowed = 10
    size = len(dataReference)
    for sampleIndex in range(size):
        phase = data[sampleIndex]
        newphase = phase

        aroundPointsReference = globals.getAroundPoints2(sampleIndex, N_lastPoints, dataReference)
        referencePhaseAverage = globals.pointsAverage(aroundPointsReference)
        distance = abs(referencePhaseAverage-phase)                               #actual distance
        # if distance < phaseMaxDifference:        #assuming the signal difference allowed be lower
            # continue
        
        increment = round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
        increasedPhaseDistance = abs(referencePhaseAverage-(phase + (increment)))
        decreasedPhaseDistance = abs(referencePhaseAverage-(phase - (increment)))
        if increasedPhaseDistance < distance*distanceImprovementFactor:
            newphase = phase+increment          #if we can make it closer to average, we do
            processed+=1
        elif decreasedPhaseDistance < distance*distanceImprovementFactor:
            newphase = phase-increment
            processed+=1
        data[sampleIndex] = newphase

    
    print("processed: ", processed)


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

sync(dataJSON, "fixedPhase", "mobilePhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)

