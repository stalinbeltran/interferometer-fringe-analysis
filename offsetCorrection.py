

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

def getRansacModel(refSection):
    refData = refSection["data"]
    refXdata = np.array(refData[dataType]["hz"])
    refYdata = np.array(refData[dataType]["deltaPhase"])
    
    X = refXdata.reshape(-1, 1)
    Y = refYdata.reshape(-1, 1)

    ransac = RANSACRegressor()
    ransac.fit(X, Y)
    return ransac


def getOffset(section, model):
    data = section["data"]
    xdata = np.array(data[dataType]["hz"]).reshape(-1, 1)
    ydata = np.array(data[dataType]["deltaPhase"])
    y_pred = model.predict(xdata).reshape(-1)
    residuals = ydata - y_pred
    average = sum(residuals)/len(ydata)
    return average


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)


dataType = "original"
newSections = []
refSection = dataJSON[referenceSectionIndex]
refSize = len(refSection["data"][dataType]["deltaPhase"])
print("data length Reference: ", refSize)
index = -1

model = getRansacModel(refSection)
for section in dataJSON:
    index +=1

    offset = getOffset(section, model)
    offset *=-1
    data = section["data"]
    hz = data[dataType]["hz"]
    ydata = getDisplacedData(data[dataType]["deltaPhase"], offset)
    data["rangeCorrected"] = {
        "deltaPhase": ydata,
        "hz": hz,
    }
    section["offset"] = offset



with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)


