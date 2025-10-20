#python3 removeNoDataPoints.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-UnwrapedNoFileInfo.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-ValidDataPoints.json 

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
for segment in segments:
    samples = segment["samples"]
    newSegmentSamples = []
    for sample in samples:
        if "timePeriod"  in sample and "hz"  in sample and "deltaPhase"  in sample and "deltaPhasePixels"  in sample :
            newSegmentSamples.append(sample)
            processed+=1
    segment["samples"] = newSegmentSamples
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)


print("processed: ", processed)