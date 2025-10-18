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
ykey = (sys.argv[3])
ykey = ykey.split(':')
phaseMaxDifference = float(sys.argv[4])             #0.1    #max allowed diff between average and a point
N_lastPoints = int(sys.argv[5])                     #40
averagePointsReference = int(sys.argv[6])           #200
distanceImprovementFactor = 0.99

def getSoftenedAverage(index, N_lastPoints, data):
    aroundPointsReference = globals.getAroundPoints2(index, N_lastPoints, data)
    signalAverage = globals.pointsAverage(aroundPointsReference)
    return signalAverage

def sync(dataJSON, phaseKeyReference, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints, averagePointsReference
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

        referenceCurveAverage = getSoftenedAverage(sampleIndex, averagePointsReference, dataReference)
        curveAverage = getSoftenedAverage(sampleIndex, averagePointsReference, data)
        difference = curveAverage - referenceCurveAverage
        referencePhaseAverage = getSoftenedAverage(sampleIndex, N_lastPoints, dataReference) + difference
        
        
        distance = abs(referencePhaseAverage-phase)                               #actual distance
        if distance < phaseMaxDifference:        #assuming the signal difference allowed be lower
            continue
        
        increment = 1 #round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
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

sync(dataJSON, ykey[0], ykey[1])


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)

