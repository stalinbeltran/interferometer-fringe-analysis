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
leftrightdifference = []
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
    leftrightdifference.append(leftImageMeanPhase - rightImageMeanPhase)
    i+=1

maxFrame = max(frameNumbers)
print(maxFrame)

MARK_NOT_EXIST = 3.5
droppedFrames = [MARK_NOT_EXIST for x in range (maxFrame)]
print(droppedFrames)
for i in range(maxFrame):
    if i+1 in frameNumbers:
        droppedFrames[i] = 4        #existence marked

print(droppedFrames)
print(frameNumbers)
allFrameNumbers = [x for x in range (1, maxFrame + 1)]

print(len(allFrameNumbers))

previouslyDropped = []
PREVIOUSFRAMES = 10
for frame in frameNumbers:
    if frame < PREVIOUSFRAMES:
        final = 0
    else:
        final = frame - PREVIOUSFRAMES
    previous = 0
    for i in range(frame - 1, final, -1):
        print(i, len(droppedFrames))
        if droppedFrames[i] == MARK_NOT_EXIST:
            previous+=1
    previouslyDropped.append(previous)

    



# ax1.plot(frameNumbers, framePhasesLeft, 'ro', markersize=3, label="Left Beam")
#ax1.plot(frameNumbers, framePhasesRight, 'go', markersize=3, label="Right Beam")
#ax1.plot(allFrameNumbers, droppedFrames, 'b-', markersize=3, label="Valid Frame")
#ax1.plot(frameNumbers, leftrightdifference, 'ro', markersize=3, label="Phase difference")
ax1.plot(previouslyDropped, leftrightdifference, 'go', markersize=3, label="previously dropped")
ax1.set_xlabel("previously dropped")
#ax1.set_ylabel("phase")
ax1.set_ylabel("phase")
plt.legend(loc="upper left")
plt.show()
