#D:\Stalin\Desarrollo\interferometer-fringe-analysis>python fitImage.py ./videos/fringes_7/framesRescaled ./videos/fringes_7/framesFitImage ./videos/fringes_7/framesFitImagejson 300

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
    leftParameters = data["fitData"][side]["fitParameters"]
    parameters = list(leftParameters[0].keys())
    parametersSize = len(parameters)
    leftParametersPhases = np.zeros(len(leftParameters))
    npParameters = np.zeros((parametersSize, len(leftParameters)))
    j = 0
    for leftParameter in leftParameters:
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
    
    
def getMean(data, filename, video_name):
    filenameParts = filename.split('-')
    #print(filenameParts)
    frameNumber = filenameParts[1]              #define the frame number is always in this position in the filename
    leftMean = getMeanBySide(data, "leftSide")
    rightMean = getMeanBySide(data, "rightSide")
    
    frame = {
        "filename": filename,
        "frameNumber": frameNumber,
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
video_name = (sys.argv[3])

frameData = []
for filename in os.listdir(input_folder):
    inputPath = os.path.join(input_folder, filename)
    data = None
    with open(inputPath, 'r') as f:
        data = json.load(f)
    if not data:
        continue
    frame = getMean(data, filename, video_name)
    frameData.append(frame)
    
with open(output_file, 'w') as f:
    json.dump(frameData, f)
