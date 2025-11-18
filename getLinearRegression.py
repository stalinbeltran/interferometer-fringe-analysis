import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

input_file = (sys.argv[1])
output_file = (sys.argv[2])
dataType = "rangeCorrected"

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

    
hz = []
deltaPhase = []
for section in dataJSON:
    data = section["data"]
    hz.extend(data[dataType]["hz"])
    deltaPhase.extend(data[dataType]["deltaPhase"])
    

print("puntos: ", len(hz))

xdata = np.array(hz)
ydata = np.array(deltaPhase)


X = xdata.reshape(-1, 1)
Y = ydata.reshape(-1, 1)
    
reg = LinearRegression().fit(X, Y)
score = reg.score(X, Y)
coefficient = reg.coef_[0][0]
intercept = reg.intercept_[0]


y_pred = reg.predict(X)

# 1. Root Mean Square Error (classical)
rmse = np.sqrt(mean_squared_error(ydata, y_pred))

linearRegression = {
    "coefficient": coefficient,
    "intercept": intercept,
    "rmse": rmse,
    "score": score,
}

print(linearRegression)

outputJSON = {
    "linearRegression":linearRegression,
    "data":{
        "hz": hz,
        "deltaPhase": deltaPhase
    }
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

