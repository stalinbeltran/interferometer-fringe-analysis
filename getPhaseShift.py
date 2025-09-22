 #python3 getPhaseShift.py ./60hzSegmentSamplesFFT.json ./60hzSegmentsSamplesPhaseShift.json 

import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]

for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        deltaPhase = None
        averagePeriod = None
        deltaPhasePixels = None
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        try:
            deltaPhase = (fileMobile["fftParams"]["phase"] - fileFixed["fftParams"]["phase"])/360       #phase in degrees, converted to fractional(0.0-1.0)
            averagePeriod = (fileMobile["fftParams"]["period"] + fileFixed["fftParams"]["period"])/2    #in case there are differences in period
            deltaPhasePixels = averagePeriod*deltaPhase                                                 #useful to compare samples by pixels
        except Exception as e:
            print(e)

        sample["deltaPhase"] = deltaPhase
        sample["averagePeriod"] = averagePeriod
        sample["deltaPhasePixels"] = deltaPhasePixels


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

