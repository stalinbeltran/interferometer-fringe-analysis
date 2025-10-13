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
distanceImprovementFactor = 0.5


def sync(segmentsJSON, phaseKeyReference, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    segments = segmentsJSON["segments"]
    processed = 0
    show = False
    showed = 0
    maxShowed = 10
    for segment in segments:
        samples = segment["samples"]
        if len(samples) == 0:
            continue
        lastPointsReference = deque(maxlen=N_lastPoints)
        lastPointsReference.append(samples[0][phaseKeyReference])
        sampleIndex = -1
        
        for sample in samples:
            sampleIndex+=1
            timestamp = sample["timestamp"]
            if phaseKey == "mobilePhase" and timestamp == "1760023379.738320":
                print("found timestamp")
                show = True
            if phaseKeyReference not in sample: continue
            if phaseKey not in sample: continue
            phase = sample[phaseKey]
            newphase = phase
            if sampleIndex > N_lastPoints:
                beginning = sampleIndex-N_lastPoints
            else:
                beginning = 0
            end = beginning + N_lastPoints
            data = [ x[phaseKeyReference] for x in samples[beginning:end] ]
            lastPointsReference = deque(maxlen=N_lastPoints)
            lastPointsReference.extend(data)
            referencePhaseAverage = globals.lastPointsAverage(lastPointsReference)
            distance = abs(referencePhaseAverage-phase)                               #actual distance
            if distance < phaseMaxDifference:        #assuming the signal difference allowed be lower
                if show and showed < maxShowed:
                    showed+=1
                    print("-----   distance < phaseMaxDifference")
                    print("-----   timestamp:", timestamp)
                    print("referencePhaseAverage: ", referencePhaseAverage)
                    print("phase:", phase)
                    print("new phase:", newphase)
                    print("distance:", distance)
                continue
            
            increment = round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
            increasedPhaseDistance = abs(referencePhaseAverage-(phase + (increment)))
            decreasedPhaseDistance = abs(referencePhaseAverage-(phase - (increment)))
            if increasedPhaseDistance < distance*distanceImprovementFactor: newphase = phase+increment          #if we can make it closer to average, we do
            elif decreasedPhaseDistance < distance*distanceImprovementFactor: newphase = phase-increment
            sample[phaseKey] = newphase
            processed+=1
            lastPointsReference.append(newphase)
            
            if show and showed < maxShowed:
                showed+=1
                print("-----   timestamp:", timestamp)
                print("referencePhaseAverage: ", referencePhaseAverage)
                print("phase:", phase)
                print("new phase:", newphase)
                print("distance:", distance)
                print("increasedPhaseDistance:", increasedPhaseDistance)
                print("decreasedPhaseDistance:", decreasedPhaseDistance) 
                    
    
    print("processed: ", processed)


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)
#sync(segmentsJSON, "deltaPhase")
sync(segmentsJSON, "fixedPhase", "mobilePhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

