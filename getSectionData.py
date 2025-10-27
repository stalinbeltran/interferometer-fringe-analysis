#python3 getSectionData.py


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


def sectionLen(section):
    return len(section["data"]["softened"]["deltaPhase"])

def sectionUpdate(section, score, coef, intercept):
    size = sectionLen(section)
    newSection = {
        "isContinuous": section["isContinuous"],
        "size": size,
        "regression": {
            "score": score,
            "coef": coef,
            "intercept": intercept
        },
        "data": {
            "original": section["data"]["original"],
            "softened": section["data"]["softened"],
        }
    }
    return newSection



with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

begin = 0
c = 0
newSections = []
for section in dataJSON:
    isContinuous = section["isContinuous"]
    if not isContinuous: continue               #ignore discontinuities
    data = section["data"]
    size = sectionLen(section)
    
    xdata = data["original"]["hz"]
    ydata = data["original"]["deltaPhase"]
    xdataNP = np.array(xdata)
    ydataNP = np.array(ydata)
    xdataNP = xdataNP.reshape(-1, 1)
    ydataNP = ydataNP.reshape(-1, 1)
    reg = LinearRegression().fit(xdataNP, ydataNP)
    score = reg.score(xdataNP, ydataNP)
    coef = reg.coef_
    intercept = reg.intercept_
    newSection = sectionUpdate(section, score, coef[0][0], intercept[0])
    newSections.append(newSection)
    



outputJSON = newSections

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

