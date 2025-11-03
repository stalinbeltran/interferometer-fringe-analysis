

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

MAX_RANGE_VALUE = 1 #arbitrary value, to uniformize ranges of values


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

def getNewSection(section, ransac):
    newSection = {
        "direction": section["direction"],
        "size":  section["size"],
        "ransac": ransac,
        "data": section["data"]
    }
    return newSection
    

newSections = []
for section in dataJSON:
    data = section["data"]
    ransac = section["ransac"]
    rangeValues = ransac["inliersRange"]
    maxValue = rangeValues["max"]
    offset = MAX_RANGE_VALUE - maxValue
    ydata = np.array(data["original"]["deltaPhase"])
    ydata = [y + offset for y in ydata]
    data["rangeCorrected"] = ydata
    break
    
    # ransac = {
        # "coefficient": coefficient,
        # "intercept": intercept,
        # "rmse": rmse,
        # "mad": mad,
        # "inlierMask": inlierMask.tolist(),
        # "inliersRange": {"max": maxValue, "min": minValue}
    # }



with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)
