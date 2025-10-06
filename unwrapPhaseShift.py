#python3 unwrapPhaseShift.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.25
phaseImprovementFactor = 0.4

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
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        timestamp = sample["timestamp"]
        if not previousSamplePhase:
            previousSamplePhase = deltaPhase
            continue
        distance = abs(previousSamplePhase-deltaPhase)
        if timestamp == "1759504001.888692": show = True
        if show:
            print("-----timestamp:", timestamp)
            print("deltaPhase:", deltaPhase)
            print("distance:", distance)
        if distance >= phaseMaxDifference:    #too much error
            increasedPhase = abs(previousSamplePhase-(deltaPhase + 1))
            decreasedPhase = abs(previousSamplePhase-(deltaPhase - 1))            
            if increasedPhase < distance: deltaPhase+=1          #if we can make it closer to average, we do
            elif decreasedPhase < distance: deltaPhase-=1
            sample["deltaPhase"] = deltaPhase
            processed+=1
        if show:
            print("deltaPhase:", deltaPhase)
            showed+=1
        if showed >= maxShowed: exit()
            #if processed >= final: break
        previousSamplePhase = deltaPhase


exit()

#check if hz adjacent has adjacent values
hzTotalAllSegments = []

for segment in segments:
    samples = segment["samples"]
    hzTotalSegment = {}
    segmentDataAverage = {"deltaPhaseTotal": 0, "n": 0}
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        segmentDataAverage["deltaPhaseTotal"] += deltaPhase
        segmentDataAverage["n"] += 1
        hz = sample["hz"]
        hzRounded = str(round(hz))
        if hzRounded not in hzTotalSegment:
            hzTotalSegment[hzRounded] = {"deltaPhaseTotal": 0, "n": 0}
        hzTotal = hzTotalSegment[hzRounded]
        hzTotal["deltaPhaseTotal"] += deltaPhase
        hzTotal["n"] += 1
        
    for key in hzTotalSegment:
        hzTotalSegment[key]["deltaPhaseAverage"] = hzTotalSegment[key]["deltaPhaseTotal"] / hzTotalSegment[key]["n"]
    hzTotalSegment["segmentDataAverage"] = segmentDataAverage["deltaPhaseTotal"]/segmentDataAverage["n"]
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
            # if distance > 1.0:
                # print(sample["timestamp"], ": ", distance)
                # break
            increasedPhase = abs(hzTotal["deltaPhaseAverage"]-(deltaPhase + 1))
            decreasedPhase = abs(hzTotal["deltaPhaseAverage"]-(deltaPhase - 1))
            if increasedPhase < distance: deltaPhase+=1          #if we can make it closer to average, we do
            elif decreasedPhase < distance: deltaPhase-=1
            sample["deltaPhase"] = deltaPhase            
            processed+=1


processed = 0
segmentIndex = 0
maxPhaseDistance = 0.2
for segment in segments:
    samples = segment["samples"]
    hzTotalSegment = hzTotalAllSegments[segmentIndex]
    segmentAverage = hzTotalSegment["segmentDataAverage"]
    print("segmentAverage:", segmentAverage)
    for sample in samples:
        if "deltaPhase" not in sample: continue
        deltaPhase = sample["deltaPhase"]
        distance = abs(segmentAverage-deltaPhase)
        #print("distance:", distance)
        if distance >= maxPhaseDistance:    #too much error
            increasedPhaseDistance = abs(segmentAverage-(deltaPhase + 1))
            decreasedPhaseDistance = abs(segmentAverage-(deltaPhase - 1))
            if decreasedPhaseDistance < distance*phaseImprovementFactor: deltaPhase+=1          #if we can make it closer to average, we do
            elif decreasedPhaseDistance < distance*phaseImprovementFactor: deltaPhase-=1
            sample["deltaPhase"] = deltaPhase            
            processed+=1
            #if processed>10: break
    #break


print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

