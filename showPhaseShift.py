#python3 showPhaseShift.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesPhaseShift.json  

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing

input_file = (sys.argv[1])

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
phases = []
for segment in segments:
    segmentPhases = []
    samples = segment["samples"]
    periods = []
    for sample in samples:
        deltaPhase = None
        deltaPhasePixels = None
        if "deltaPhase" not in sample or sample["deltaPhase"] is None: continue
        deltaPhase = sample["deltaPhase"]
        if deltaPhase is None: continue
        amplitude = 1           #only sign is used in getProcessedPhase(), so a positive value is enough
        deltaPhase, amplitude = phaseProcessing.getProcessedPhase(deltaPhase*2*np.pi, amplitude)
        deltaPhase = deltaPhase/(2*np.pi)
        phases.append(deltaPhase)
        segmentPhases.append(deltaPhase)
        # except Exception as e:
            # print(e)

    #histogram.showHistogram(segmentPhases, "Phases")
histogram.showHistogram(phases, "Phases")


