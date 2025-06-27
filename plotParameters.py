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

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 1)
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xticks([])
ax1.set_yticks([])

data = None
with open(archivoProcesar, 'r') as f:
    data = json.load(f)
if not data:
    sys.exit()
size = len(data)
frameNumbers = np.zeros(size)
framePhasesLeft = np.zeros(size)
framePhasesRight = np.zeros(size)
i = 0
for frame in data:
    frameNumber = frame["frameNumber"]
    frameNumbers[i] = frameNumber
    leftImageMean = frame["leftImage"]["mean"]
    rightImageMean = frame["rightImage"]["mean"]
    leftImageMeanPhase = leftImageMean["phase"]
    rightImageMeanPhase = rightImageMean["phase"]
    framePhasesLeft[i] = leftImageMeanPhase
    framePhasesRight[i] = rightImageMeanPhase
    i+=1

ax1.plot(frameNumbers, framePhasesLeft, 'r-')
ax1.plot(frameNumbers, framePhasesRight, 'g-')

plt.show()
