#python3 showPhaseShift.py ./60hzSegmentsSamplesPhaseShift.json 
#python3 showPhaseShift.py ./40hzSegmentsSamplesPhaseShift.json 

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
        averagePeriod = None
        deltaPhasePixels = None
        try:
            deltaPhase = sample["deltaPhase"]
            if deltaPhase is None: continue            
            averagePeriod = sample["averagePeriod"]
            periods.append(averagePeriod)
            amplitude = 1           #only sign is used in getProcessedPhase(), so a positive value is enough
            deltaPhase, amplitude = phaseProcessing.getProcessedPhase(deltaPhase*2*np.pi, amplitude)
            deltaPhase = deltaPhase/(2*np.pi)
            phases.append(deltaPhase)
            segmentPhases.append(deltaPhase)
        except Exception as e:
            print(e)

    histogram.showHistogram(periods, "Periods")
    histogram.showHistogram(segmentPhases, "Phases")
histogram.showHistogram(phases, "Phases")


