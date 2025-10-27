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
keyx = globals.getPromptOptionalParameter(5, [{"func": globals.split, "funcParams": [":"]}])

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

begin = 0
c = 0
totalSize = 0
maximumSize = 0
minumumSize = 0
title = input_file
plt.title(title)
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
    totalSize += dataSize
    end = begin + dataSize
    xdata = range(begin, end)
    if keyx:            
        xdata = data[dataType][keyx[0]]
    if not marker:
        marker = '.'
        if isContinuous:
            marker = '-'
        
    plt.plot(xdata, ydata, marker)
    begin = end
    c+=1
    if totalSize > 100000:
        plt.show()
        totalSize = 0

plt.show()
