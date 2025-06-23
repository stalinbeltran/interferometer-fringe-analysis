import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import cv2
from scipy.signal import find_peaks
from scipy.ndimage.filters import gaussian_filter1d
import sys

archivoProcesar = sys.argv[1]
print('file:',archivoProcesar)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_yticks([])
ax2.set_xticks([])

img = cv2.imread(archivoProcesar, 0) # read in the image as grayscale

ax1.imshow(img, cmap='gray')
ax1.set_title("Original image (grayscale)")

img[img < 10] = 0 # apply some arbitrary thresholding (there's
# a bunch of noise in the image

yp, xp = np.where(img != 0)

xmax = max(xp)
xmin = min(xp)
target_slice = (xmax - xmin)*.75 + xmin # get the middle of the fringe blob

sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5) # get the vertical derivative

sobely = cv2.blur(sobely,(7,7)) # make the peaks a little smoother

ax2.imshow(sobely, cmap='gray') #show the derivative (troughs are very visible)
ax2.plot([target_slice, target_slice], [img.shape[0], 0], 'r-')

def findPeaks(slc):
    peaks = find_peaks(slc)[0] # [0] returns only locations 
    i = 0
    size = np.size(peaks)
    wavelength = np.empty(size)
    for i in range(1, size):
        wavelength[i-1] = peaks[i] - peaks[i-1]
    return wavelength

def getWavelength(xmiddle, xmax):
    wavelengths = np.empty(0)
    for target_slice in range(xmiddle, xmax):
        slc = sobely[:, int(target_slice)]
        slc[slc < 0] = 0
        ax2.set_title("vertical derivative (red line indicating slice taken from image)")

        slc = gaussian_filter1d(slc, sigma=10) # filter the peaks the remove noise,
        # again an arbitrary threshold

        ax3.plot(slc) 
        wavelength = findPeaks(slc)
        np.resize(wavelengths, np.size(wavelength))
        wavelengths = np.append(wavelengths, wavelength)
        
        slc *=-1
        wavelength = findPeaks(slc)
        np.resize(wavelengths, np.size(wavelength))
        wavelengths = np.append(wavelengths, wavelength)

    print('wavelengths size:', np.size(wavelengths))
    print('mean:', np.mean(wavelengths))
    print('std:', np.std(wavelengths))
    
print()
xmiddle = int((xmax - xmin)*.5)
print('Left image:')
getWavelength(xmin, xmiddle - 1)
print()
print('Right image:')
getWavelength(xmiddle, xmax)
#ax3.plot(peaks, slc[peaks], 'ro')
#ax3.set_title('number of fringes: ' + str(len(peaks)))
#plt.show()
