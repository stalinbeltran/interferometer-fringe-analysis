 #python3 showPhaseShift.py ./60hzSegmentsSamplesPhaseShift.json 

import os
import sys
import json
import cv2
import numpy as np
import histogram

input_file = (sys.argv[1])

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
phases = []
for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        deltaPhase = None
        averagePeriod = None
        deltaPhasePixels = None
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        try:
            deltaPhase = sample["deltaPhase"]
            if deltaPhase is None: continue
            phases.append(deltaPhase)
        except Exception as e:
            print(e)

histogram.showHistogram(phases, "Phases")


