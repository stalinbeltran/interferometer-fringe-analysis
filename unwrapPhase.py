#python3 unwrapPhase.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PlainData.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseCorrection.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseUnwrapped.json 

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
phaseCorrectionFile = (sys.argv[2])
output_file = (sys.argv[3])



with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)
    
with open(phaseCorrectionFile, 'r', encoding='utf-8') as f:
    phaseCorrectionJSON = json.load(f)

results = phaseCorrectionJSON
original = dataJSON[0]["data"]

for key in results:
    previousPhase = 0
    data = original[key]
    begin = 0
    for result in results[key]:
        section = result["section"]
        phaseIncrement = result["localPhaseCorrection"]
        previousPhase += phaseIncrement
        end = begin + len(section)
        for i in range(begin, end):
            data[i] += previousPhase
        begin = end



outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

