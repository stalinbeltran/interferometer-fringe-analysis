#showSections.py


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

input_file = (sys.argv[1])
dataType = (sys.argv[2])
sectionSizeRange = globals.getPromptOptionalParameter(3, [{"func": globals.split, "funcParams": [":"]}, {"func": int}])
marker = globals.getPromptOptionalParameter(4)
positionRange = globals.getPromptOptionalParameter(5, [{"func": globals.split, "funcParams": [":"]}, {"func": int}])
keyx = globals.getPromptOptionalParameter(6)
sectionsShowed = globals.getPromptOptionalParameter(7, int)

if not marker:
    marker = '.'
            
with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

begin = 0
totalSize = 0
maximumSize = 0
minumumSize = 0
title = input_file
plt.title(title)
#plt.xlim(4.5, 7.5) 
sectionCounter = 0
if sectionSizeRange:
    print("sectionSizeRange: ", sectionSizeRange)
    minumumSize = sectionSizeRange[0]
    maximumSize = sectionSizeRange[1]
for section in dataJSON:
    data = section["data"]
    sectionSize = section["size"]
    if maximumSize > 0 and sectionSize > maximumSize: continue
    if minumumSize > 0 and sectionSize < minumumSize: continue

    ydata = data[dataType]["deltaPhase"]
    dataSize = len(ydata)
    totalSize += dataSize
    end = begin + dataSize
    if positionRange:
        if positionRange[0]>0 and end < positionRange[0]:
            begin = end
            continue
        if positionRange[1]>0 and begin > positionRange[1]:
            begin = end
            continue

    if keyx is None or keyx == "SEQUENTIAL":
        xdata = [x for x in range(begin, end)]
    else:
        xdata = data[dataType][keyx]

        
    plt.plot(xdata, ydata, marker)
    begin = end
    sectionCounter +=1
    if sectionsShowed and sectionCounter % sectionsShowed == 0:
        plt.show()
if totalSize > 0: 
    plt.show()
