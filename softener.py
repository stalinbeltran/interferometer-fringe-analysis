#python3 softener.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-NoFileInfo.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseSoften.json

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.9
minimumDataSize = 100           #minumum data points for apply softening

def isContinuous(value, lastValue):
    global phaseMaxDifference
    if abs(value-lastValue) > phaseMaxDifference: return False
    return True


def softenSamples(samples, phaseKey):
    signal = []
    for sample in samples:                  #get values
        if phaseKey in sample:
            signal.append(sample[phaseKey])
    filteredSignal = globals.filter(signal, cutoff = 25)    #filer noise
    size = len(filteredSignal)
    for i in range(0, size):
        sample = samples[i]
        if phaseKey in sample:
            sample[phaseKey] = filteredSignal[i]    #replace older values
        


def softenSignal(segmentsJSON, phaseKey):
    global minimumDataSize
    
    segments = segmentsJSON["segments"]
    processed = 0
    for segment in segments:
        samples = segment["samples"]
        previousSamplePhase = None
        if len(samples)==0: continue
        sample = samples[0]
        lastValue = sample[phaseKey]
        data = []
        acceptIrregular = True
        for sample in samples:
            data.append(sample)                                     #always accept the present sample, even if it is the last one
            if phaseKey in sample:
                value = sample[phaseKey]
            else:
                print(sample)
                continue
                
            valueIsContinuous = isContinuous(value, lastValue)
            lastValue = value
            
            if acceptIrregular and valueIsContinuous and len(data) > minimumDataSize:           #acceptIrregularities until first not irregular value is found
                acceptIrregular = False
            if not acceptIrregular and not valueIsContinuous:       #found first discontinuity after some nice continuity
                softenSamples(data, phaseKey)                       #apply softening
                                                                    #and restart data collection
                data = []
                acceptIrregular = True
            
            
            


    
    print("processed: ", processed)
   


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

softenSignal(segmentsJSON, "deltaPhase")
softenSignal(segmentsJSON, "mobilePhase")
softenSignal(segmentsJSON, "fixedPhase")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

