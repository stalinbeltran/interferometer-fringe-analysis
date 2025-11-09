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
dataType = "original"

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)


if not dataType:
    dataType = "original"
    
xdata = []
ydata = []
for section in dataJSON:
    data = section["data"]
    xdata.extend(data[dataType]["hz"])
    ydata.extend(data[dataType]["deltaPhase"])
    

xdata = np.array(xdata)
ydata = np.array(ydata)

X = xdata.reshape(-1, 1)
Y = ydata.reshape(-1, 1)
    
reg = LinearRegression().fit(X, Y)
score = reg.score(X, Y)
coefficient = reg.coef_[0][0]
intercept = reg.intercept_[0]

linearRegression = {
    "coefficient": coefficient,
    "intercept": intercept,
    "score": score,
}

print(linearRegression)

outputJSON = linearRegression

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

