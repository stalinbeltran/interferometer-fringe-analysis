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
        mobilePhase = None
        fixedPhase = None
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        if "period" not in fileMobile or "period" not in fileFixed or fileMobile["period"] is None or fileFixed["period"] is None: continue
        try:
            mobilePhase = fileMobile["period"]["phase"]
            fixedPhase = fileFixed["period"]["phase"]
            deltaPhase = (mobilePhase - fixedPhase)       #phase in degrees, converted to fractional(0.0-1.0)            
            deltaPhase = phaseProcessing.getPositivePhaseDegrees(deltaPhase)/360
            deltaPhasePixels = fileMobile["period"]["period"]*deltaPhase                                                 #useful to compare samples by pixels
            mobilePhase = mobilePhase/360
            fixedPhase = fixedPhase/360
            processed+=1
        except Exception as e:
            print(e)

        sample["deltaPhase"] = deltaPhase
        sample["deltaPhasePixels"] = deltaPhasePixels
        sample["mobilePhase"] = mobilePhase
        sample["fixedPhase"] = fixedPhase

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)


print("processed: ", processed)