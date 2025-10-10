#python3 unwrapPhaseShift.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.20
distanceImprovementFactor = 0.9
N_lastPoints = 8

def lastPointsAverage(lastPoints):
    average = sum(lastPoints) / len(lastPoints)
    #print("average:", average)
    return average



def unwrapPhaseShift(segmentsJSON, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    segments = segmentsJSON["segments"]
    processed = 0
    show = False
    showed = 0
    maxShowed = 20
    for segment in segments:
        samples = segment["samples"]
        previousSamplePhase = None
        lastPoints = deque(maxlen=N_lastPoints)
        for sample in samples:
            if phaseKey not in sample: continue
            phase = sample[phaseKey]
            timestamp = sample["timestamp"]
            if timestamp == "1760016259.756601": #"1760016262.002568":
                show = True
            if not previousSamplePhase:
                lastPoints.append(phase)
                previousSamplePhase = lastPointsAverage(lastPoints)
                continue
            
            if show:
                print("previousSamplePhase: ", previousSamplePhase)
            distance = abs(previousSamplePhase-phase)
            if distance >= phaseMaxDifference:    #too much error
                increasedPhaseDistance = abs(previousSamplePhase-(phase + 1))
                decreasedPhaseDistance = abs(previousSamplePhase-(phase - 1))
                if show:
                    print("-----timestamp:", timestamp)
                    print("phase:", phase)
                    print("distance:", distance)
                    print("increasedPhaseDistance:", increasedPhaseDistance)
                    print("decreasedPhaseDistance:", decreasedPhaseDistance) 
                if increasedPhaseDistance < distance*distanceImprovementFactor: phase+=1          #if we can make it closer to average, we do
                elif decreasedPhaseDistance < distance*distanceImprovementFactor: phase-=1
                sample[phaseKey] = phase
                processed+=1
            if show:
                showed+=1
            if show and showed >= maxShowed:
                show = False
            lastPoints.append(phase)
            previousSamplePhase = lastPointsAverage(lastPoints)
    
    print("processed: ", processed)


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)
unwrapPhaseShift(segmentsJSON, "deltaPhase")
unwrapPhaseShift(segmentsJSON, "mobilePhase")
unwrapPhaseShift(segmentsJSON, "fixedPhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

