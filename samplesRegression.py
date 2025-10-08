#python3 samplesRegression.py D:\Stalin\FotosFranjasProyecto\results\tuesday07102025-ValidDataPoints.json D:\Stalin\FotosFranjasProyecto\results\tuesday07102025-SamplesRegression.json 100

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
output_file = (sys.argv[2])
REGRESSION_SIZE = int(sys.argv[3])


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

processed = 0
segments = segmentsJSON["segments"]
for segment in segments:
    segmentHz = []
    segmentPhases = []
    segmentTimestamps = []
    samples = segment["samples"]
    periods = []
    firstRegressionTimestamp = None
    segmentRegressions = []
    for sample in samples:
        deltaPhase = None
        hz = sample["hz"]
        deltaPhase = sample["deltaPhase"]
        if not firstRegressionTimestamp:
            firstRegressionTimestamp = sample["timestamp"]
            #print("First timestamp: ", firstRegressionTimestamp)
        processed+=1
        segmentHz.append(hz)
        segmentPhases.append(deltaPhase)
        segmentTimestamps.append(float(sample["timestamp"]))
        if processed % REGRESSION_SIZE == 0:
            m, b = np.polyfit(segmentHz, segmentPhases, 1)
            regression = {"firstRegressionTimestamp": firstRegressionTimestamp, "m": m, "b": b}
            segmentRegressions.append(regression)
            segmentHz = []
            segmentPhases = []
            segmentTimestamps = []
            firstRegressionTimestamp = None
    segment["regressions"] = segmentRegressions

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)
