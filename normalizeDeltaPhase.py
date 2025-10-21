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
# standardValue = float(sys.argv[3])
# offsetValue = int(sys.argv[4])
phaseMaxDifference = 0.1
samples = 1800

def processData(hz, data, divider, offset):
    global samples
    
    print("divider: ", divider)
    print("offset: ", offset)
    size = samples
    #size = len(hz)
    hzModified = np.zeros(size)
    processed = 0
    for i in range(size):
        phase = data[i]
        hzModified[i] = -hz[i]/divider + offset
        referenceValue = hzModified[i]
        distance = abs(referenceValue-phase)                               #actual distance
        # if distance < phaseMaxDifference:        #assuming the signal difference allowed be lower
            # continue
        newphase = phase
        increment = round(distance)                                             #only increment/decrement an integer number of times, to keep phase information
        increasedPhaseDistance = abs(referenceValue-(phase + (increment)))
        decreasedPhaseDistance = abs(referenceValue-(phase - (increment)))
        if increasedPhaseDistance < distance:
            newphase = phase+increment          #if we can make it closer to average, we do
            processed+=1
        elif decreasedPhaseDistance < distance:
            newphase = phase-increment
            processed+=1
        data[i] = newphase

    xdata = range(size)
    ydata = data[:size]
    ydata2 = hzModified[:size]
    
    #plt.plot(xdata, ydata2, '.', label='ds')
    plt.plot(xdata, ydata, '.', label='ds')
    plt.show()



with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

hz = dataJSON[0]["data"]["hz"]
data = dataJSON[0]["data"]["deltaPhase"]          #first element is the original (unmodified) data


# for i in range(0, 1):
    # for j in range(0, 10):

# for j in range(0, 1):
    # for i in range(0, -10, -1):
    
for j in range(0, 1):
    for i in range(0, -10, -1):
        divider = 0.74 + i/25
        offset = 2.0 + j/10
        processData(hz, data, divider, offset)
        print()

# dataJSON[0]["data"]["hzModified"] = hzModified.tolist()
# with open(output_file, 'w', encoding='utf-8') as f:
    # json.dump(dataJSON, f, ensure_ascii=False, indent=4)

#print("processed: ", processed)
