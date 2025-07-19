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
import math

archivoProcesar = sys.argv[1]
data = None
with open(archivoProcesar, 'r') as f:
    data = json.load( f)

phases = []
for framedata in data:
    phase = framedata["phase"]["value"]
    amplitude = framedata["amplitude"]["value"]
    factor = abs(math.trunc(phase/(2*np.pi)))
    if phase < 0: phase += (factor + 1)*2*np.pi         #avoid negative phases
    if phase > 2*np.pi: phase -= factor*2*np.pi
    
    # if amplitude < 0:
        # if phase < 0:
            # phase += (factor + 1)*2*np.pi
    # factor = abs(math.trunc(phase/(2*np.pi)))

    phases.append(phase)
hist.showHistogram(phases)

# frequency = params["frequency"]["value"]
# wavelength = 2*np.pi/frequency

