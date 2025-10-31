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
keyx = globals.getPromptOptionalParameter(6, [{"func": globals.split, "funcParams": [":"]}])

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
plt.xlim(4.5, 7.5) 
if sectionSizeRange:
    print("sectionSizeRange: ", sectionSizeRange)
    minumumSize = sectionSizeRange[0]
    maximumSize = sectionSizeRange[1]
for section in dataJSON:
    isContinuous = section["isContinuous"]
    if not isContinuous:
        # print(" coef: ", section["regression"]["coef"], " size: ", section["size"])
        continue
    data = section["data"]
    sectionSize = section["size"]
    if maximumSize > 0 and sectionSize > maximumSize: continue
    if minumumSize > 0 and sectionSize < minumumSize: continue

    ydata = data[dataType]["deltaPhase"]
    dataSize = len(ydata)
    print("dataSize: ", dataSize)
    totalSize += dataSize
    end = begin + dataSize
    if positionRange:
        if positionRange[0]>0 and end < positionRange[0]: continue
        if positionRange[1]>0 and begin > positionRange[1]: continue
    xdata = range(begin, end)
    if keyx:            
        xdata = data[dataType][keyx[0]]

        
    plt.plot(xdata, ydata, marker)
    plt.show()
    begin = end
    # if positionRange and totalSize > positionRange[1] and positionRange[1] and begin <= positionRange[1]  > 0:
        # plt.show()
if totalSize > 0: 
    plt.show()
