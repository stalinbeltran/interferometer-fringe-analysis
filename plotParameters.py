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
frameNumbers = range(1,size+1)
framePhasesLeft = np.zeros(size)
framePhasesRight = np.zeros(size)
i = 0
for frame in data:
    frameNumber = frame["frameNumber"]
    #frameNumbers[i] = frameNumber
    leftImageMean = frame["leftImage"]["mean"]
    rightImageMean = frame["rightImage"]["mean"]
    leftImageMeanPhase = leftImageMean["phase"]
    rightImageMeanPhase = rightImageMean["phase"]
    framePhasesLeft[frameNumber-1] = leftImageMeanPhase
    framePhasesRight[frameNumber-1] = rightImageMeanPhase
    i+=1


x = np.linspace(0, 10, 30)
y = np.sin(x)

#plt.plot(x, y, 'o', markersize=3, color='black');
ax1.plot(frameNumbers, framePhasesLeft, 'ro', markersize=3, label="Left Beam")
ax1.plot(frameNumbers, framePhasesRight, 'go', markersize=3, label="Right Beam")
ax1.set_xlabel("video frame")
ax1.set_ylabel("phase")
plt.legend(loc="upper left")
plt.show()
