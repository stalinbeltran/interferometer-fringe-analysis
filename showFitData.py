#python3 showFitData.py ./videos/fringes_44/framesLeftEqualized/fitData.json

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
import histogram as hist
import phaseProcessing as pp

archivoProcesar = sys.argv[1]
data = None
with open(archivoProcesar, 'r') as f:
    data = json.load( f)

phases = []
for framedata in data:
    phase = framedata["phase"]["value"]
    amplitude = framedata["amplitude"]["value"]
    phase, amplitude = pp.getProcessedPhase(phase, amplitude)
    phases.append(phase)
hist.showHistogram(phases)


