#python3 getSectionsHz.py


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
output_file = (sys.argv[2])

UP = "UP"
DOWN = "DOWN"
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
        if direction == UP:
            if actualValue > lastValue:
                lastValue = actualValue
            if lastValue - actualValue > MINIMUM_DISTANCE : break
        if direction == DOWN:
            if actualValue < lastValue:
                    lastValue = actualValue
            if actualValue - lastValue > MINIMUM_DISTANCE : break
    return (begin, end)
            

            
def getNewSection(original, softened, sectionRange, direction):
    size = len(original["hz"][sectionRange[0]:sectionRange[1]])
    newSection = {
        "direction": direction,
        "size": size,
        "data": {
            "original": {
                "hz": original["hz"][sectionRange[0]:sectionRange[1]],
                "deltaPhase": original["deltaPhase"][sectionRange[0]:sectionRange[1]]
            }, 
            "softened": {
                "hz": softened["hz"][sectionRange[0]:sectionRange[1]],
                "deltaPhase": softened["deltaPhase"][sectionRange[0]:sectionRange[1]]
            }
        }
    }
    return newSection




with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

original = dataJSON[0]["data"]      #take the original data
softened = dataJSON[1]["data"]          #take the softened data
hz = softened["hz"]
size = len(hz)

begin = 0    
newSections = []
for i in range(size):
    while begin + 1 < size:
        direction = getDirection(hz, begin)                       #find actual direction (UP or DOWN)
        if direction is None:
            begin += 1
            continue
        sectionRange = getDirectionRange(hz, direction, begin)    #get the range where this direction is valid
        newSection = getNewSection(original, softened, sectionRange, direction)              #create new section with this data range
        newSections.append(newSection)
        end = sectionRange[1]
        begin = end
    
    


outputJSON = newSections

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)




