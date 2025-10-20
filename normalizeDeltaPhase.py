#python3 normalizeDeltaPhase.py 


import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
output_file = (sys.argv[2])
standardValue = float(sys.argv[3])
offsetValue = int(sys.argv[4])
phaseMaxDifference = 0.1

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

hz = dataJSON[0]["data"]["hz"]
data = dataJSON[0]["data"]["deltaPhase"]          #first element is the original (unmodified) data

size = len(hz)
hzModified = np.zeros(size)
for i in range(size):
    hzModified[i] = -hz[i]/1.5 + 3

# processed = 0
# pointIndex = -1
# for phase in data:
    # pointIndex +=1
    # distance = abs(standardValue-phase)                               #actual distance
    # if distance < phaseMaxDifference:        #assuming the signal difference allowed be lower
        # continue
    # newphase = phase
    # increment = round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
    # increasedPhaseDistance = abs(standardValue-(phase + (increment)))
    # decreasedPhaseDistance = abs(standardValue-(phase - (increment)))
    # if increasedPhaseDistance < distance:
        # newphase = phase+increment          #if we can make it closer to average, we do
        # processed+=1
    # elif decreasedPhaseDistance < distance:
        # newphase = phase-increment
        # processed+=1
    # data[pointIndex] = newphase


dataJSON[0]["data"]["hzModified"] = hzModified.tolist()

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)

#print("processed: ", processed)
