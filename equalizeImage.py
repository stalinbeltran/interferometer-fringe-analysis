#python3 equalizeImage.py ./images/fringes_44-1-.png

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
print('file:',archivoProcesar)
guessedWavelength = 100

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_yticks([])
ax2.set_xticks([])

img = cv2.imread(archivoProcesar, 0) # read in the image as grayscale

yp, xp = np.where(img != 0)
xmax = max(xp)
xmin = min(xp)
ax1.imshow(img, cmap='gray') #show the derivative (troughs are very visible)
ax1.set_title("original: " + archivoProcesar)

print()

filenameNoExt, file_extension = os.path.splitext(archivoProcesar)
outputFile = os.path.join(filenameNoExt + "_equalized" + file_extension)

imgnew = isf.getHorizontalMean(img)
params = isf.verticalSineFit(img, guessedWavelength)
print(params)
frequency = params["frequency"]["value"]
wavelength = 2*np.pi/frequency
print("wavelength: " + str(wavelength))

ax2.imshow(imgnew, cmap='gray')
ax2.set_title("New image")
plt.show()
