#python3 checkFile.py D:\Stalin\FotosFranjasProyecto\results\tuesday07102025-Segments.json D:\Stalin\FotosFranjasProyecto\results\tuesday07102025-SegmentsChecked.json

import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def checkFile(imagePath):
    try:
        image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        if image is None: return None
        else: return image        
    except:
        return None


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
for segment in segments:
    #segment["files"].append(file)
    files = segment["files"]
    newSegmentFiles = []
    for file in files:
        image = checkFile(file["absolutePath"])
        if image is not None:               #the image file is openable
            newSegmentFiles.append(file)
        processed+=1
        #if processed > 2: break
    segment["files"] = newSegmentFiles
    #break

print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)
