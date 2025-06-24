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
gs = gridspec.GridSpec(3, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])
ax4 = fig.add_subplot(gs[2, :])
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_yticks([])
ax2.set_xticks([])

img = cv2.imread(archivoProcesar, 0) # read in the image as grayscale

ax1.imshow(img, cmap='gray')
ax1.set_title("Original image")

#img[img < 10] = 0 # apply some arbitrary thresholding (there's
# a bunch of noise in the image

yp, xp = np.where(img != 0)

xmax = max(xp)
xmin = min(xp)
target_slice = (xmax - xmin)*.75 + xmin # get the middle of the fringe blob

sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5) # get the vertical derivative

sobely = cv2.blur(sobely,(7,7)) # make the peaks a little smoother

ax2.imshow(sobely, cmap='gray') #show the derivative (troughs are very visible)
ax2.set_title("vertical derivative")

def findPeaks(slc):
    peaks = find_peaks(slc)[0] # [0] returns only locations
    return peaks
    
def getWavelengthArray(peaks):
    size = np.size(peaks)
    wavelength = np.empty(size - 1)
    for i in range(1, size):
        wavelength[i-1] = peaks[i] - peaks[i-1]
    #print(wavelength)
    return wavelength
    

def getPhaseArray(peaks, wavelength, negativeFunction):
    print('getPhaseArray')
    size = np.size(peaks)
    phase = np.empty(size)
    for i in range(size):
        phase[i] = peaks[i]/wavelength%1.0
        if negativeFunction:
            phase[i]+=0.25      #as the negative function will have a pi/2 phase offset, we add it to compensate
            phase[i] = phase[i]%1.0     #and avoid values over 1
        print('phase[i]', phase[i])
    return phase

def processSliceWavelength(slc, wavelengths):
    peaks = findPeaks(slc)
    if np.size(peaks)<2:
	    return wavelengths
    wavelength = getWavelengthArray(peaks)
    np.resize(wavelengths, np.size(wavelengths) + np.size(wavelength))
    wavelengths = np.append(wavelengths, wavelength)
    return wavelengths
    
    
def processSlicePhase(slc, phases, wavelength, negative = False):
    peaks = findPeaks(slc)
    print('peaks', peaks)
    if np.size(peaks)<1:
        return phases
    print('before getPhaseArray')
    phase = getPhaseArray(peaks, wavelength, negative)
    np.resize(phases, np.size(phases) + np.size(phase))
    phases = np.append(phases, phase)
    return phases

def scanImageWavelengths(xbegin, xend, axis):
    wavelengths = np.empty(0)
    
    for target_slice in range(xbegin, xend):
        slc = sobely[:, int(target_slice)]
        #slc[slc < 0] = 0
        #slc = gaussian_filter1d(slc, sigma=10) # filter the peaks the remove noise, again an arbitrary threshold
        axis.plot(slc)
        
        wavelengths = processSliceWavelength(slc, wavelengths)
        slc *=-1                    #get the negative of the slice to work the minimums too
        wavelengths = processSliceWavelength(slc, wavelengths)


    mean = np.mean(wavelengths)
    std = np.std(wavelengths)
    return mean, std, wavelengths
    

def scanImagePhases(xbegin, xend, wavelength):
    phases = np.empty(0)
    for target_slice in range(xbegin, xend):
        slc = sobely[:, int(target_slice)]
        #print('slc', slc)
        #slc[slc < 0] = 0
        #print('slc0', slc)
        #slc = gaussian_filter1d(slc, sigma=10) # filter the peaks the remove noise,
        # again an arbitrary threshold
        
        phases = processSlicePhase(slc, phases, wavelength)
        slc *=-1                    #get the negative of the slice to work the minimums
        phases = processSlicePhase(slc, phases, wavelength, True)

    mean = np.mean(phases)
    std = np.std(phases)
    return mean, std, phases
    
    
print()
xmiddle = int((xmax - xmin)*.5)
print('Left image:')
meanWavelength, stdWavelength, wavelengths = scanImageWavelengths(xmin, xmiddle - 1, ax3)
print('wavelengths size:', np.size(wavelengths))
print(wavelengths)
print('mean wavelength:', meanWavelength)
print('std wavelength:', stdWavelength)


meanPhase, stdPhase, phases = scanImagePhases(xmin, xmiddle - 1, meanWavelength)
print('phases size:', np.size(phases))
print(phases)
print('mean phase:', meanPhase)
print('std phase:', stdPhase)
ax3.set_title("Left Image (Wavelength: " + ' mean: ' + "{:.1f}".format(meanWavelength) + ' std: ' + "{:.1f}".format(stdWavelength) + ") (Phase: " + ' mean: ' + "{:.2f}".format(meanPhase) + ' std: ' + "{:.2f}".format(stdPhase) + ")")
    

    
print()
print('Right image:')
meanWavelength, stdWavelength, wavelengths = scanImageWavelengths(xmiddle, xmax, ax4)
print('wavelengths size:', np.size(wavelengths))
print(wavelengths)
print('mean wavelength:', meanWavelength)
print('std wavelength:', stdWavelength)
ax4.set_title("Right Image Wavelength" + ' mean: ' + "{:.1f}".format(meanWavelength) + ' std: ' + "{:.1f}".format(stdWavelength) )


meanPhase, stdPhase, phases = scanImagePhases(xmiddle, xmax, meanWavelength)
print('phases size:', np.size(phases))
print(phases)
print('mean phase:', meanPhase)
print('std phase:', stdPhase)
ax4.set_title("Right Image (Wavelength: " + ' mean: ' + "{:.1f}".format(meanWavelength) + ' std: ' + "{:.1f}".format(stdWavelength) + ") (Phase: " + ' mean: ' + "{:.2f}".format(meanPhase) + ' std: ' + "{:.2f}".format(stdPhase) + ")")

#ax3.set_title('number of fringes: ' + str(len(peaks)))
plt.show()
