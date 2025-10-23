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
maximumSize = globals.getPromptOptionalParameter(3, int)
minumumSize = globals.getPromptOptionalParameter(4, int)

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

begin = 0
c = 0
totalSize = 0
for section in dataJSON:
    isContinuous = section["isContinuous"]
    data = section["data"]
    sectionSize = section["size"]
    if maximumSize and maximumSize > 0 and sectionSize > maximumSize: continue
    if minumumSize and minumumSize > 0 and sectionSize < minumumSize: continue
    
    
    totalSize += sectionSize
    end = begin + sectionSize
    xdata = range(begin, end)
    ydata = data[dataType]["deltaPhase"]
    marker = '.'
    if isContinuous: marker = '-'
    plt.plot(xdata, ydata, marker)
    begin = end
    c+=1
    if totalSize > 3000:
        plt.show()
        totalSize = 0

plt.show()
