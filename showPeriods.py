#python3 showPeriods.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesFirstPeriod.json

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import globals

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def countPeriods(value, previousPeriodsCounters):
    for period in previousPeriodsCounters:
        if period["period"] == value:
            periodFound = period
            periodFound["count"] +=1
            return
    periodFound = {"period": value, "count": 1}
    previousPeriodsCounters.append(periodFound)
        
    


def getLookedPeriod(previousPeriodsCounters):
    maximumPeriod = globals.WIDTH/4                 #do not take photos with less than 4 fringes
    previousPeriodsCountersSorted = sorted(previousPeriodsCounters, key=lambda x: x['count'])
    for period in previousPeriodsCountersSorted:
        if period["period"] > maximumPeriod: continue
        return period["period"]
    return None

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

with open(output_file, 'w', encoding='utf-8') as f:         #verify it is openable
    pass

segments = segmentsJSON["segments"]
processed = 0
nulls = 0
periods = []
for segment in segments:
    samples = segment["samples"]
    segmentPeriod = []
    previousPeriodsCounters = []
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        try:
            periods.append(fileMobile["period"]["period"])
            countPeriods(periods[-1], previousPeriodsCounters)
            periods.append(fileFixed["period"]["period"])
            countPeriods(periods[-1], previousPeriodsCounters)
        except:
            nulls +=1
            continue
            
        segmentPeriod.append(fileMobile["period"]["period"])
        segmentPeriod.append(fileFixed["period"]["period"])            
        processed+=2
        #if processed > 5: break
    #histogram.showHistogram(segmentPeriod, "segment periods")
    print("------segment timestamp: ", segment["timestamp"])
    print("previousPeriodsCounters: ", previousPeriodsCounters)
    segment["periodsCounter"] = {"periodsCounter": previousPeriodsCounters}
    segment["lookedPeriod"] = getLookedPeriod(previousPeriodsCounters)
    
    
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

print("nulls: ", nulls)
histogram.showHistogram(periods, label = ["Periods"])


