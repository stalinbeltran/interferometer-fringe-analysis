#python equalizeImage.py ./images/alineacion666_rescaled.png 250


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import cv2
from scipy.signal import find_peaks
from scipy.ndimage.filters import gaussian_filter1d
import sys
import os
from scipy.optimize import curve_fit
import sineEqualizer as se

archivoProcesar = sys.argv[1]
guessedWavelength = float(sys.argv[2])
print('file:',archivoProcesar)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(3, 2)
ax1 = fig.add_subplot(gs[0, 1])
ax2 = fig.add_subplot(gs[0, 0])
ax3 = fig.add_subplot(gs[1, :])
ax4 = fig.add_subplot(gs[2, :])
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_yticks([])
ax2.set_xticks([])

img = cv2.imread(archivoProcesar, 0) # read in the image as grayscale
imgnew = img
yp, xp = np.where(img != 0)
xmax = max(xp)
xmin = min(xp)
ax2.imshow(img, cmap='gray') #show the derivative (troughs are very visible)
ax2.set_title("original: " + archivoProcesar)

se.imageEqualize(archivoProcesar, guessedWavelength)
sys.exit()


print()
xmiddle = int((xmax - xmin)/2)
meanPhase, stdPhase, phases, paramListLeft = scanImage(0, xmiddle, ax3)
print('phases size:', np.size(phases))
print('mean phase:', meanPhase)
print('std phase:', stdPhase)

meanPhase, stdPhase, phases, paramListRight = scanImage(xmiddle, xmax, ax4)
print('phases size:', np.size(phases))
print('mean phase:', meanPhase)
print('std phase:', stdPhase)
#print('paramList:', paramList)
ax3.set_title("Left Image")
ax4.set_title("Right Image")

filenameNoExt, file_extension = os.path.splitext(archivoProcesar)
outputPath = os.path.join(filenameNoExt + "_equalized" + file_extension)
img2 = imgnew
cv2.imwrite(outputPath, img2)
ax1.imshow(imgnew, cmap='gray')
ax1.set_title("New image")
plt.show()
