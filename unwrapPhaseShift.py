#python3 unwrapPhaseShift.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.25
distanceImprovementFactor = 0.9
N_lastPoints = 8

def lastPointsAverage(lastPoints):
    average = sum(lastPoints) / len(lastPoints)
    #print("average:", average)
    return average




with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
inicio = 650
final = inicio + 1
processed = 0
show = False
showed = 0
maxShowed = 4
for segment in segments:
    samples = segment["samples"]
    previousSamplePhase = None
    lastPoints = deque(maxlen=N_lastPoints)
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        timestamp = sample["timestamp"]
        if not previousSamplePhase:
            previousSamplePhase = deltaPhase
            continue
        distance = abs(previousSamplePhase-deltaPhase)
        if timestamp == "1759504798.269329":
            show = False
        if distance >= phaseMaxDifference:    #too much error
            increasedPhaseDistance = abs(previousSamplePhase-(deltaPhase + 1))
            decreasedPhaseDistance = abs(previousSamplePhase-(deltaPhase - 1))
            if show:
                print("-----timestamp:", timestamp)
                print("deltaPhase:", deltaPhase)
                print("distance:", distance)
                print("increasedPhaseDistance:", increasedPhaseDistance)
                print("decreasedPhaseDistance:", decreasedPhaseDistance) 
            if increasedPhaseDistance < distance*distanceImprovementFactor: deltaPhase+=1          #if we can make it closer to average, we do
            elif decreasedPhaseDistance < distance*distanceImprovementFactor: deltaPhase-=1
            sample["deltaPhase"] = deltaPhase
            processed+=1
        if show:
            print("final deltaPhase:", deltaPhase)
            showed+=1
        if showed >= maxShowed: exit()
            #if processed >= final: break
        lastPoints.append(deltaPhase)
        previousSamplePhase = lastPointsAverage(lastPoints)


print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

