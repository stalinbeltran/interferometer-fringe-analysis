#python3 unwrapPhase.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.2                #max allowed diff between average and a point
distanceImprovementFactor = 0.9
N_lastPoints = 16


def unwrapPhase(segmentsJSON, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    segments = segmentsJSON["segments"]
    processed = 0
    show = False
    showed = 0
    maxShowed = 4
    for segment in segments:
        samples = segment["samples"]
        aroundPoints = deque(maxlen=N_lastPoints)
        if len(samples) == 0:
            continue
        averageSamplePhase = samples[0][phaseKey]
        aroundPoints.append(averageSamplePhase)
        sampleIndex = -1
        
        for sample in samples:
            sampleIndex+=1
            phase = sample[phaseKey]
            newphase = phase
            aroundPoints = globals.getAroundPoints(sampleIndex, N_lastPoints, samples, phaseKey)
            averageSamplePhase = globals.pointsAverage(aroundPoints)
            
            distance = abs(averageSamplePhase-phase)
            if distance < phaseMaxDifference:
                aroundPoints.append(phase)
                continue
            
            increment = round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
            increasedPhaseDistance = abs(averageSamplePhase-(phase + (increment)))
            decreasedPhaseDistance = abs(averageSamplePhase-(phase - (increment)))
            if increasedPhaseDistance < distance*distanceImprovementFactor: newphase = phase+increment          #if we can make it closer to average, we do
            elif decreasedPhaseDistance < distance*distanceImprovementFactor: newphase = phase-increment
            sample[phaseKey] = newphase
            processed+=1
            aroundPoints.append(newphase)
            
            timestamp = sample["timestamp"]
            if phaseKey == "mobilePhase" and timestamp == "xxxxx1760020163.209353":
                show = True
            if show and showed < maxShowed:
                showed+=1
                print("averageSamplePhase: ", averageSamplePhase)
                print("new phase:", newphase)
                print("-----   timestamp:", timestamp)
                print("phase:", phase)
                print("distance:", distance)
                print("increasedPhaseDistance:", increasedPhaseDistance)
                print("decreasedPhaseDistance:", decreasedPhaseDistance) 
                    
    
    print("processed: ", processed)


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)
unwrapPhase(segmentsJSON, "mobilePhase")
unwrapPhase(segmentsJSON, "fixedPhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

