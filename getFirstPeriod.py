#python3 getFirstPeriod.py D:\Stalin\FotosFranjasProyecto\viernesXXX\results\40hzSegmentSamplesPeriodPhase.json D:\Stalin\FotosFranjasProyecto\viernesXXX\results\40hzSegmentSamplesFirstPeriod.json


import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getFirstPeriod(periods):
    return periods[0]



with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        if "period" not in fileMobile:
            fileMobile["period"] = getFirstPeriod(fileMobile["periods"])
            processed+=1

        if "period" not in fileFixed:
            fileFixed["period"] = getFirstPeriod(fileFixed["periods"])
            processed+=1
        if processed > 10: break
print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)
