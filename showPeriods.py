#python3 showPeriods.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesFirstPeriod.json

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing

input_file = (sys.argv[1])

def countPeriods(value):
    global previousPeriods, periodsCounter
    if value not in previousPeriods:
        previousPeriods.append(value)
        periodsCounter[value] = 1
    else:
        periodsCounter[value] += 1



with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
nulls = 0
periods = []
for segment in segments:
    samples = segment["samples"]
    segmentPeriod = []
    previousPeriods = []
    periodsCounter = {}
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        try:
            periods.append(fileMobile["period"]["period"])
            countPeriods(periods[-1])
            periods.append(fileFixed["period"]["period"])
            countPeriods(periods[-1])
        except:
            nulls +=1
            continue
            
        segmentPeriod.append(fileMobile["period"]["period"])
        segmentPeriod.append(fileFixed["period"]["period"])            
        processed+=2
        #if processed > 5: break
    #histogram.showHistogram(segmentPeriod, "segment periods")
    print("------segment timestamp: ", segment["timestamp"])
    print("periodsCounter: ", periodsCounter)
    
print("nulls: ", nulls)
histogram.showHistogram(periods, label = ["1", "2"])


