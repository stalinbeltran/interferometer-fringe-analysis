#python3 unwrapPhaseShift.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.25

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
inicio = 650
final = inicio + 1
processed = 0
for segment in segments:
    samples = segment["samples"]
    previousSamplePhase = None
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        if previousSamplePhase and abs(previousSamplePhase-deltaPhase) >= phaseMaxDifference:    #too much error
            if deltaPhase < previousSamplePhase and deltaPhase < 0.6 and abs(deltaPhase + 1 - previousSamplePhase) < phaseMaxDifference: deltaPhase+=1          #adjust one wavelength more or less
            elif deltaPhase > previousSamplePhase and deltaPhase >= 1 and abs(deltaPhase - 1 - previousSamplePhase) < phaseMaxDifference: deltaPhase-=1
            sample["deltaPhase"] = deltaPhase
            processed+=1
            #if processed >= final: break
        previousSamplePhase = deltaPhase

#check if hz adjacent has adjacent values
hzTotalAllSegments = []
for segment in segments:
    samples = segment["samples"]
    hzTotalSegment = {}
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        hz = sample["hz"]
        hzRounded = str(round(hz))
        if hzRounded not in hzTotalSegment:
            hzTotalSegment[hzRounded] = {"deltaPhaseTotal": 0, "n": 0}
        hzTotal = hzTotalSegment[hzRounded]
        hzTotal["deltaPhaseTotal"] += deltaPhase
        hzTotal["n"] += 1
        
    for key in hzTotalSegment:
        hzTotalSegment[key]["deltaPhaseAverage"] = hzTotalSegment[key]["deltaPhaseTotal"] / hzTotalSegment[key]["n"]
    hzTotalAllSegments.append(hzTotalSegment)

print(hzTotalAllSegments)


processed = 0
segmentIndex = 0
maxPhaseDistance = 0.5
for segment in segments:
    samples = segment["samples"]
    hzTotalSegment = hzTotalAllSegments[segmentIndex]
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        hz = sample["hz"]
        hzRounded = str(round(hz))
        hzTotal = hzTotalSegment[hzRounded]
        distance = abs(hzTotal["deltaPhaseAverage"]-deltaPhase)
        if distance >= maxPhaseDistance:    #too much error
            if abs(hzTotal["deltaPhaseAverage"]-deltaPhase + 1) < maxPhaseDistance: deltaPhase+=1          #if we can make it closer to average, we do
            elif abs(hzTotal["deltaPhaseAverage"]-deltaPhase - 1) < maxPhaseDistance: deltaPhase-=1
            sample["deltaPhase"] = deltaPhase            
            processed+=1



print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

