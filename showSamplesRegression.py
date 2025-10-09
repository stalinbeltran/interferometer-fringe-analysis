#python3 showSamplesRegression.py D:\Stalin\FotosFranjasProyecto\results\tuesday07102025-SamplesRegression.json

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

processed = 0
timestamps = []
ms = []
segments = segmentsJSON["segments"]
for segment in segments:
    segmentRegressions = segment["regressions"]
    for regression in segmentRegressions:
        timestamps.append(float(regression["firstRegressionTimestamp"]))
        ms.append(regression["m"])

size = len(timestamps)
x = range(1, size)

m, b = np.polyfit(timestamps, ms, 1)
print("m: ", m, "    b: ",b)
histogram.showHistogram(ms, label= "Phases")
if False:
    plt.plot(timestamps, ms, '.')
    plt.plot(timestamps, ms, '.')
plt.show()
