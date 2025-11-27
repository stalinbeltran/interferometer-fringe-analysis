import os
import sys
import json
import cv2
import numpy as np
import globals


input_file = (sys.argv[1])
output_file = (sys.argv[2])
dataType = "rangeCorrected"

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

    
hz = []
deltaPhase = []
for section in dataJSON:
    data = section["data"]
    hz.extend(data[dataType]["hz"])
    deltaPhase.extend(data[dataType]["deltaPhase"])


size = len(hz)
print("size: ", size)
text = "hz, deltaPhase\n"
for i in range(size):
    text += str(hz[i]) + "," + str(deltaPhase[i]) + "\n"

with open(output_file, 'w') as f:
    f.write(text)

