#python3 removeFileInfo.py D:\Stalin\FotosFranjasProyecto\results\friday03102025-PhaseShiftUnwraped.json D:\Stalin\FotosFranjasProyecto\results\friday03102025-UnwrapedNoFileInfo.json 

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
        if "fileMobileMirror" in sample:
            del sample["fileMobileMirror"]
        if "fileFixedMirror" in sample:
            del sample["fileFixedMirror"]
        processed+=1

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

