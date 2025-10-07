#python3 getPhaseShift.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesDefinitivePeriod.json D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesPhaseShift.json 

import os
import sys
import json
import cv2
import numpy as np
import phaseProcessing

input_file = (sys.argv[1])
output_file = (sys.argv[2])

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]

processed = 0
for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        deltaPhase = None
        deltaPhasePixels = None
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        if "period" not in fileMobile or "period" not in fileFixed or fileMobile["period"] is None or fileFixed["period"] is None: continue
        try:
            deltaPhase = (fileMobile["period"]["phase"] - fileFixed["period"]["phase"])       #phase in degrees, converted to fractional(0.0-1.0)            
            deltaPhase = phaseProcessing.getPositivePhaseDegrees(deltaPhase)/360
            deltaPhasePixels = fileMobile["period"]["period"]*deltaPhase                                                 #useful to compare samples by pixels
            if sample["timestamp"] == "1759500293.119290":
                print("deltaPhase: ", deltaPhase)
            processed+=1
        except Exception as e:
            print(e)

        sample["deltaPhase"] = deltaPhase
        sample["deltaPhasePixels"] = deltaPhasePixels

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

