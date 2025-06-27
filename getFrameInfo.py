#python getFrameInfo.py ./videos/fringes_7/framesFitImagejson ./videos/fringes_7/infoFrames.json

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys
import os
import imageSineFit as isf
import json
import numpy as np


def getMeanBySide(data, side):
    sideParameters = data["fitData"][side]["fitParameters"]
    parameters = list(sideParameters[0].keys())
    parametersSize = len(parameters)
    leftParametersPhases = np.zeros(len(sideParameters))
    npParameters = np.zeros((parametersSize, len(sideParameters)))
    j = 0
    for leftParameter in sideParameters:
        for i in range(parametersSize):
            npParameters[i][j] = leftParameter[parameters[i]]["value"]
        j +=1
        
    mean = np.mean(npParameters, axis = 1)
    i = 0
    f = {}
    for param in parameters:
        f[param] = mean[i]
        i+=1
    return f
    
    
def getMean(data, filename):
    filenameParts = filename.split('-')
    #print(filenameParts)
    frameNumber = filenameParts[1]              #define the frame number is always in this position in the filename
    leftMean = getMeanBySide(data, "leftSide")
    rightMean = getMeanBySide(data, "rightSide")
    
    frame = {
        "filename": filename,
        "frameNumber": int(frameNumber),
        "leftImage":{
            "mean":leftMean
        },
        "rightImage":{
            "mean":rightMean
        }
    }

    return frame




input_folder = (sys.argv[1])
output_file = (sys.argv[2])

frameData = []
for filename in os.listdir(input_folder):
    inputPath = os.path.join(input_folder, filename)
    data = None
    with open(inputPath, 'r') as f:
        data = json.load(f)
    if not data:
        continue
    frame = getMean(data, filename)
    frameData.append(frame)
    
with open(output_file, 'w') as f:
    json.dump(frameData, f)
