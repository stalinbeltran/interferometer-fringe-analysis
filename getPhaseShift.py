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
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        deltaPhase = (fileMobile["fftParams"]["phase"] - fileFixed["fftParams"]["phase"])/360
        averagePeriod = (fileMobile["fftParams"]["period"] + fileFixed["fftParams"]["period"])/2
        deltaPhasePixels = averagePeriod*deltaPhase
        sample["deltaPhase"] = deltaPhase
        sample["averagePeriod"] = averagePeriod
        sample["deltaPhasePixels"] = deltaPhasePixels
        break
    break

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

