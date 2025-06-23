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

def findPeaks(slc):
    peaks = find_peaks(slc)[0] # [0] returns only locations
    ax3.plot(peaks, slc[peaks], 'ro')
    return peaks
    
def getWavelengthArray(peaks):
    size = np.size(peaks)
    wavelength = np.empty(size - 1)
    for i in range(1, size):
        wavelength[i-1] = peaks[i] - peaks[i-1]
    #print(wavelength)
    return wavelength
    

def getPhaseArray(peaks, wavelength):
    size = np.size(peaks)
    phase = np.empty(size)
    for i in range(size):
        phase[i] = peaks[i]/wavelength%1.0
    return phase

def processSliceWavelength(slc, wavelengths):
    peaks = findPeaks(slc)
    wavelength = getWavelengthArray(peaks)
    np.resize(wavelengths, np.size(wavelengths) + np.size(wavelength))
    wavelengths = np.append(wavelengths, wavelength)
    return wavelengths
    
    
def processSlicePhase(slc, phases, wavelength):
    peaks = findPeaks(slc)
    phase = getPhaseArray(peaks, wavelength)
    np.resize(phases, np.size(phases) + np.size(phase))
    phases = np.append(phases, phase)
    return phases

def scanImageWavelengths(xbegin, xend):
    wavelengths = np.empty(0)
    for target_slice in range(xbegin, xend):
        slc = sobely[:, int(target_slice)]
        slc[slc < 0] = 0
        ax2.set_title("vertical derivative (red line indicating slice taken from image)")

        slc = gaussian_filter1d(slc, sigma=10) # filter the peaks the remove noise,
        # again an arbitrary threshold

        
        ax2.plot([target_slice, target_slice], [img.shape[0], 0], 'r-')
        ax3.plot(slc)
        
        wavelengths = processSliceWavelength(slc, wavelengths)
        slc *=-1                    #get the negative of the slice to work the minimums
        wavelengths = processSliceWavelength(slc, wavelengths)


    mean = np.mean(wavelengths)
    std = np.std(wavelengths)
    return mean, std, wavelengths
    

def scanImagePhases(xbegin, xend, wavelength):
    phases = np.empty(0)
    for target_slice in range(xbegin, xend):
        slc = sobely[:, int(target_slice)]
        slc[slc < 0] = 0
        ax2.set_title("vertical derivative (red line indicating slice taken from image)")

        slc = gaussian_filter1d(slc, sigma=10) # filter the peaks the remove noise,
        # again an arbitrary threshold
        
        phases = processSlicePhase(slc, phases, wavelength)
        slc *=-1                    #get the negative of the slice to work the minimums
        phases = processSlicePhase(slc, phases, wavelength)

    mean = np.mean(phases)
    std = np.std(phases)
    return mean, std, phases
    
    
print()
xmiddle = int((xmax - xmin)*.5)
print('Left image:')
meanWavelength, stdWavelength, wavelengths = scanImageWavelengths(xmin, xmiddle - 1)
print('wavelengths size:', np.size(wavelengths))
print(wavelengths)
print('mean wavelength:', meanWavelength)
print('std wavelength:', stdWavelength)


meanPhase, stdPhase, phases = scanImagePhases(xmin, xmiddle - 1, meanWavelength)
print('phases size:', np.size(phases))
print(phases)
print('mean phase:', meanPhase)
print('std phase:', stdPhase)
    
print()
print('Right image:')
#scanImageWavelengths(xmiddle, xmax)
#ax3.set_title('number of fringes: ' + str(len(peaks)))
#plt.show()
