#python3 unwrapPhaseShift.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-SegmentSamplesPhaseShift.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json 

import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])
phaseMaxDifference = 0.5

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
        #if (processed > inicio and processed < final): print("deltaPhase: ", deltaPhase, "previousSamplePhase: ", previousSamplePhase)
        if previousSamplePhase and abs(previousSamplePhase-deltaPhase) >= phaseMaxDifference:    #too much error
            if deltaPhase < previousSamplePhase and deltaPhase < 0.4: deltaPhase+=1          #adjust one wavelength more or less
            elif deltaPhase > previousSamplePhase and deltaPhase > 1: deltaPhase-=1          #adjust one wavelength more or less
            #elif deltaPhase > previousSamplePhase: deltaPhase+=1
            sample["deltaPhase"] = deltaPhase
            #if (processed > inicio and processed < final): print("corrected: ", deltaPhase)
            processed+=1
            #if processed >= final: break
        previousSamplePhase = deltaPhase

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

