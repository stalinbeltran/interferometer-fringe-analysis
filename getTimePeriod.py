#python3 getTimePeriod.py D:\Stalin\FotosFranjasProyecto\wednesday24092025\results\60-50limitSegmentSamples.json  D:\Stalin\FotosFranjasProyecto\wednesday24092025\results\60-50limitSegmentTimePeriod.json



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
    previousSampleTimestamp = None
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        timestamp = float(sample["timestamp"])
        if previousSampleTimestamp:
            sample["timePeriod"] = timestamp - previousSampleTimestamp
            sample["hz"] = 1.0/sample["timePeriod"]
        previousSampleTimestamp = timestamp
        #if processed > 10: break
print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)
