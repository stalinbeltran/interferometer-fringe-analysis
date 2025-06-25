#python equalizeImage.py ./images/alineacion666_rescaled.png


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import cv2
from scipy.signal import find_peaks
from scipy.ndimage.filters import gaussian_filter1d
import sys
from scipy.optimize import curve_fit

archivoProcesar = sys.argv[1]
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
target_slice = (xmax - xmin)*.75 + xmin # get the middle of the fringe blob

sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5) # get the vertical derivative

sobely = cv2.blur(sobely,(7,7)) # make the peaks a little smoother

ax2.imshow(img, cmap='gray') #show the derivative (troughs are very visible)
ax2.set_title("original: " + archivoProcesar)

def findPeaks(slc):
    peaks = find_peaks(slc)[0] # [0] returns only locations
    return peaks
    

def sine_function(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

def scanImage(xbegin, xend, axis):
    wavelengths = np.empty(0)
    cont = 0
    paramsList = []
    for target_slice in range(xbegin, xend):
        #print('target_slice', target_slice)
        slc = img[:, int(target_slice)]
        slc1 = gaussian_filter1d(slc, sigma=10) # filter the peaks the remove noise, again an arbitrary threshold
        # axis.plot(slc)
        # axis.plot(slc1)
        #ax2.plot([target_slice, target_slice], [img.shape[0], 0], 'r-')
        

        # Initial guess for the parameters [A, B, C, D]
        initial_guess = [250, np.pi/40, 0.5, 0]

        len = np.size(slc)
        x = range(0, len)
        # Perform the curve fitting
        params, covariance = curve_fit(sine_function, x, slc, p0=initial_guess)
        paramsList.append(params)
        # Extract the fitted parameters
        A_fit, B_fit, C_fit, D_fit = params

        #print(f"Fitted parameters: A={A_fit}, B={B_fit}, C={C_fit}, D={D_fit}")
        # Generate y values using the fitted parameters
        y_fit = sine_function(x, A_fit, B_fit, C_fit, D_fit)
        axis.plot(x, y_fit)
        imgnew[:, int(target_slice)] = y_fit
        cont+=1
    return paramsList
  
    
    
print()
xmiddle = int((xmax - xmin)/2)
paramListLeft = scanImage(0, xmiddle, ax3)
paramListRight = scanImage(xmiddle, xmax, ax4)
#print('paramList:', paramList)
ax3.set_title("Left Image")
ax4.set_title("Right Image")

ax1.imshow(imgnew, cmap='gray')
ax1.set_title("New image")
plt.show()
