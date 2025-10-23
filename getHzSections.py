#python3 getHzSections.py


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
output_file = (sys.argv[2])

UP = 1
DOWN = 0
MINIMUM_DISTANCE = 0.05

def getDirection(data, begin):
    size = len(data)
    firstValue = data[begin]
    direction = None
    for i in range(begin + 1, size):
        actualValue = data[i]
        if abs(actualValue - firstValue) < MINIMUM_DISTANCE: continue
        direction = DOWN
        if firstValue < actualValue: direction = UP         #up
        break
    return direction
    
    
def getDirectionRange(data, direction, begin):
    size = len(data)
    lastValue = data[begin]
    for i in range(begin, size):
        actualValue = data[i]
        end = i
        if direction == UP and lastValue > actualValue: break
        if direction == DOWN and lastValue < actualValue: break
        lastValue = actualValue
    return (begin, end)
            
            
            
            
def getNewSection(section, sectionRange):
    newSection = {
        "isContinuous": section["isContinuous"],
        "size": len(section["data"]["original"]["hz"][sectionRange[0]:sectionRange[1]]),
        "data": {
            "original": {
                "hz": section["data"]["original"]["hz"][sectionRange[0]:sectionRange[1]],
                "deltaPhase": section["data"]["original"]["deltaPhase"][sectionRange[0]:sectionRange[1]]
            }, 
            "softened": {
                "hz": section["data"]["softened"]["hz"][sectionRange[0]:sectionRange[1]],
                "deltaPhase": section["data"]["softened"]["deltaPhase"][sectionRange[0]:sectionRange[1]]
            }
        }
    }
    return newSection





with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

begin = 0
c = 0
newSections = []
for section in dataJSON:
    begin = 0
    size = section["size"]
    data = section["data"]["softened"]["hz"]
    while begin + 1 < size:
        direction = getDirection(data, begin)                       #find actual direction (UP or DOWN)
        if direction is None: continue
        sectionRange = getDirectionRange(data, direction, begin)    #get the range where this direction is valid
        newSection = getNewSection(section, sectionRange)              #create new section with this data range
        newSections.append(newSection)
        end = sectionRange[1]
        begin = end
    



outputJSON = newSections

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

