#python3 removeSlowPoints.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-ValidDataPoints.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-FastDataPoints.json 

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
        if "hz" in sample and sample["hz"] >= 4 and sample["hz"] < 6:
            newSegmentSamples.append(sample)
            processed+=1
            
    segment["samples"] = newSegmentSamples

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

