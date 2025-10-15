#python3 removeUnusedData.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-UnwrapedNoFileInfo.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-ValidDataPoints.json 

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
processed = 0
newSegments = []
for segment in segments:
    del segment["periodsCounter"]
    del segment["lookedPeriod"]
    samples = segment["samples"]
    if len(samples) == 0: continue
    newSegments.append(segment)
    for sample in samples:
        del sample["timePeriod"]
        del sample["deltaPhase"]
        del sample["deltaPhasePixels"]
        processed+=1
segmentsJSON["segments"] = newSegments


print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

