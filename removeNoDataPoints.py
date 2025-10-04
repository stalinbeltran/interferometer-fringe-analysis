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
    for sample in samples:
        if "timePeriod" not in sample or "hz" not in sample or "deltaPhase" not in sample or "deltaPhasePixels" not in sample :
            samples.remove(sample)
            continue
        processed+=1

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

