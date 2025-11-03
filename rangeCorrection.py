

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
    xdata = np.array(data["original"]["hz"])
    ydata = np.array(data["original"]["deltaPhase"])
    X = xdata.reshape(-1, 1)
    Y = ydata.reshape(-1, 1)

    # ransac = {
        # "coefficient": coefficient,
        # "intercept": intercept,
        # "rmse": rmse,
        # "mad": mad,
        # "inlierMask": inlierMask.tolist(),
        # "inliersRange": {"max": maxValue, "min": minValue}
    # }
    s = getNewSection(section, ransac)
    newSections.append(s)


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(newSections, f, ensure_ascii=False, indent=4)
