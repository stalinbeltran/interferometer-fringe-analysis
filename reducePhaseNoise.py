#python3 reducePhaseNoise.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseUnwrapped.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-reducedPhaseNoise.json 

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.5                #max allowed diff between average and a point
distanceImprovementFactor = 1
N_lastPoints = 6


def reducePhaseNoise(segmentsJSON, phaseKey):
    global phaseMaxDifference, distanceImprovementFactor, N_lastPoints
    segments = segmentsJSON["segments"]
    processed = 0
    show = False
    showed = 0
    maxShowed = 4
    for segment in segments:
        samples = segment["samples"]
        if len(samples) == 0:
            continue
        sampleIndex = -1
        for sample in samples:
            sampleIndex+=1
            phase = sample[phaseKey]
            newphase = phase
            aroundPoints = globals.getAroundPoints(sampleIndex, N_lastPoints, samples, phaseKey)
            averageSamplePhase = globals.pointsAverage(aroundPoints)
            
            distance = abs(averageSamplePhase-phase)
            if distance < phaseMaxDifference:
                continue
            
            increment = 1                                            #only increment/decrement an integer number of times, to keep phase information
            increasedPhaseDistance = abs(averageSamplePhase-(phase + (increment)))
            decreasedPhaseDistance = abs(averageSamplePhase-(phase - (increment)))
            if increasedPhaseDistance < distance*distanceImprovementFactor:
                newphase = phase+increment          #if we can make it closer to average, we do
                sample[phaseKey] = newphase
                processed+=1
            elif decreasedPhaseDistance < distance*distanceImprovementFactor:
                newphase = phase-increment
                sample[phaseKey] = newphase
                processed+=1
            
            timestamp = sample["timestamp"]
            if phaseKey == "mobilePhase" and timestamp == "1760020163.209353":
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
reducePhaseNoise(segmentsJSON, "mobilePhase")
reducePhaseNoise(segmentsJSON, "fixedPhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

