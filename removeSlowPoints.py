#python3 removeSlowPoints.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-ValidDataPoints.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-FastDataPoints.json 

import os
import sys
import json
import cv2
import numpy as np
import globals

input_file = (sys.argv[1])
output_file = (sys.argv[2])
minimumMaximumHzRange = globals.getPromptOptionalParameter(3, [{"func": globals.split, "funcParams": [":"]}, {"func": float}])
print("minimumMaximumHzRange: ", minimumMaximumHzRange)

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
minimum = minimumMaximumHzRange[0]
maximum = minimumMaximumHzRange[1]
for segment in segments:
    samples = segment["samples"]
    newSegmentSamples = []
    for sample in samples:
        if "hz" in sample and sample["hz"] >= minimum and sample["hz"] <= maximum: #remove only slowers and fasters, if any
            newSegmentSamples.append(sample)
            processed+=1
            
    segment["samples"] = newSegmentSamples

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)


print("processed: ", processed)