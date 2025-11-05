

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt
from sklearn.linear_model import RANSACRegressor, LinearRegression
from sklearn.metrics import mean_squared_error

input_file = (sys.argv[1])
output_file = (sys.argv[2])
referenceSectionIndex = globals.getPromptOptionalParameter(3, int)
ACCEPTANCE_LEVEL = globals.getPromptOptionalParameter(4, float)



def getNewSection(section, ransac):
    newSection = {
        "direction": section["direction"],
        "size":  section["size"],
        "ransac": ransac,
        "data": section["data"]
    }
    return newSection

def getDisplacedData(ydata, offset):
    ydataNew = [y + offset for y in ydata]
    return ydataNew

def getOffsetMAD(section, refSection, offset):
    refData = refSection["data"]
    refXdata = np.array(refData[dataType]["hz"])
    refYdata = np.array(refData[dataType]["deltaPhase"])
    
    data = section["data"]
    xdata = np.array(data[dataType]["hz"])
    ydata = np.array(getDisplacedData(data[dataType]["deltaPhase"], offset))
    xtotalData = np.concatenate((xdata, refXdata))
    ytotalData = np.concatenate((ydata, refYdata))
    
    X = xtotalData.reshape(-1, 1)
    Y = ytotalData.reshape(-1, 1)

    ransac = RANSACRegressor()
    ransac.fit(X, Y)
    y_pred = ransac.predict(X)
    # print("y_pred: ", y_pred)
    # print("y_pred: ", y_pred)

    # Residuals (inliers only)
    inlierMask = ransac.inlier_mask_
    residuals = ytotalData[inlierMask] - y_pred[inlierMask]

    # 2. Median Absolute Deviation (robust)
    mad = 1.4826 * np.median(np.abs(residuals - np.median(residuals)))
    return mad


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)


dataType = "original"
newSections = []
refSection = dataJSON[referenceSectionIndex]
refSize = len(refSection["data"][dataType]["deltaPhase"])
print("data length Reference: ", refSize)
index = -1
for section in dataJSON:
    index +=1
    if index == referenceSectionIndex:
        continue
    deltaOffset = 1
    offset = 0
    direction = 1
    mad = getOffsetMAD(section, refSection, offset)
    #print("mad: ", mad)
    section["madToRefStart"] = mad
    while True:
        offset += deltaOffset*direction
        newMad = getOffsetMAD(section, refSection, offset)
        if abs(mad - newMad) < ACCEPTANCE_LEVEL:
            break                  #have reached the acceptance level
        if newMad < mad:
            mad = newMad
            continue
        if deltaOffset < ACCEPTANCE_LEVEL:      #too small deltaOffset
            break
        direction *= -1
        deltaOffset /=2.0
    data = section["data"]
    hz = data[dataType]["hz"]
    ydata = getDisplacedData(data[dataType]["deltaPhase"], offset)
    data["rangeCorrected"] = {
        "deltaPhase": ydata,
        "hz": hz,
    }
    section["madToRefEnd"] = newMad
    section["madImprovement"] = section["madToRefEnd"] - section["madToRefStart"]
    if index > 5:
        break

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)
