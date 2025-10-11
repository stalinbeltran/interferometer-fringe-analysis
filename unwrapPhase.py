#python3 unwrapPhase.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.4                #max allowed diff between average and a point
distanceImprovementFactor = 0.9
N_lastPoints = 12

def lastPointsAverage(lastPoints):
    average = sum(lastPoints) / len(lastPoints)
    return average

def isPhaseBorder(phase):
    periods = round(phase)
    if abs(phase-periods) < 0.05:           #phase is in the border
        return True
    return False
    
def unwrapPhase(segmentsJSON, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    segments = segmentsJSON["segments"]
    processed = 0
    show = False
    showed = 0
    maxShowed = 4
    for segment in segments:
        samples = segment["samples"]
        previousSamplePhase = samples[0][phaseKey]
        lastPoints = deque(maxlen=N_lastPoints)
        lastPoints.append(previousSamplePhase)
        for sample in samples:
            if phaseKey not in sample: continue
            phase = sample[phaseKey]
            newphase = phase
            lastPoints.append(phase)
            if not isPhaseBorder(phase):        #from here only phase borders
                continue
            
            previousSamplePhase = lastPointsAverage(lastPoints)
            distance = abs(previousSamplePhase-phase)                               #actual distance
            increment = round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
            increasedPhaseDistance = abs(previousSamplePhase-(phase + (increment)))
            decreasedPhaseDistance = abs(previousSamplePhase-(phase - (increment)))
            if increasedPhaseDistance < distance*distanceImprovementFactor: newphase = phase+increment          #if we can make it closer to average, we do
            elif decreasedPhaseDistance < distance*distanceImprovementFactor: newphase = phase-increment
            sample[phaseKey] = newphase
            processed+=1
            
            
            timestamp = sample["timestamp"]
            if phaseKey == "mobilePhase" and timestamp == "1760016262.842869": #"1760016262.002568":
                show = True
            if show and showed < maxShowed:
                showed+=1
                print("previousSamplePhase: ", previousSamplePhase)
                print("new phase:", newphase)
                print("-----   timestamp:", timestamp)
                print("phase:", phase)
                print("distance:", distance)
                print("increasedPhaseDistance:", increasedPhaseDistance)
                print("decreasedPhaseDistance:", decreasedPhaseDistance) 
                    
    
    print("processed: ", processed)


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)
unwrapPhase(segmentsJSON, "deltaPhase")
unwrapPhase(segmentsJSON, "mobilePhase")
unwrapPhase(segmentsJSON, "fixedPhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

