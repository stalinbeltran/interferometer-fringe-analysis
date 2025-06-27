#python plotParameters.py ./videos/fringes_7/infoFrames.json


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import cv2
from scipy.signal import find_peaks
from scipy.ndimage.filters import gaussian_filter1d
import sys
import os
from scipy.optimize import curve_fit
import imageSineFit as isf
import json

archivoProcesar = sys.argv[1]

fig = plt.figure(tight_layout=False)
gs = gridspec.GridSpec(1, 1)
ax1 = fig.add_subplot(gs[0, 0])


data = None
with open(archivoProcesar, 'r') as f:
    data = json.load(f)
if not data:
    sys.exit()
size = len(data)
frameNumbers = []
framePhasesLeft = []
framePhasesRight = []
i = 0
for frame in data:
    frameNumber = frame["frameNumber"]
    frameNumbers.append(frameNumber)
    leftImageMean = frame["leftImage"]["mean"]
    rightImageMean = frame["rightImage"]["mean"]
    leftImageMeanPhase = leftImageMean["phase"]
    rightImageMeanPhase = rightImageMean["phase"]
    framePhasesLeft.append(leftImageMeanPhase)
    framePhasesRight.append(rightImageMeanPhase)
    i+=1

#del frameNumbers[15]
maxFrame = max(frameNumbers)
print(maxFrame)
droppedFrames = [-3 for x in range (maxFrame)]
print(droppedFrames)
for i in range(maxFrame):
    if i+1 in frameNumbers:
        droppedFrames[i] = -2        #existence marked

print(droppedFrames)
print(frameNumbers)
allFrameNumbers = [x for x in range (1, maxFrame + 1)]

print(len(allFrameNumbers))

ax1.plot(frameNumbers, framePhasesLeft, 'ro', markersize=3, label="Left Beam")
ax1.plot(frameNumbers, framePhasesRight, 'go', markersize=3, label="Right Beam")
ax1.plot(allFrameNumbers, droppedFrames, 'b-', markersize=3, label="Valid Frame")
ax1.set_xlabel("video frame")
ax1.set_ylabel("phase")
plt.legend(loc="upper left")
plt.show()
