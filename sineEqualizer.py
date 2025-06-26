#python equalizeImage.py ./images/alineacion666_rescaled.png 250

import numpy as np
import cv2
import os
from scipy.optimize import curve_fit

def sine_function(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

def scanImage(img, xbegin, xend, guessedParameters, imgnew):
    paramsList = []
    for target_slice in range(xbegin, xend):
        slc = img[:, int(target_slice)]             #take a slice to process
        
        # Initial guess for the parameters [A, B, C, D]
        guessedWavelength = guessedParameters.guessedWavelength
        initial_guess = [250, 2*np.pi/guessedWavelength, 0.5, 0]

        # Perform the curve fitting
        try:
            params, covariance = curve_fit(sine_function, x, slc, p0=initial_guess)
        except:
            continue    #if no fit, left slice unchanged, no fit getted
            
        paramsList.append(params)
        A_fit, B_fit, C_fit, D_fit = params     # Extract the fitted parameters
        y_fit = sine_function(x, A_fit, B_fit, C_fit, D_fit)    # Generate y values using the fitted parameters
        imgnew[:, int(target_slice)] = y_fit            #modify image with the best fit found
        
    return imgnew, paramsList 
  
def imageEqualize(archivoProcesar, guessedWavelength):
    img = cv2.imread(archivoProcesar, cv2.IMREAD_GRAYSCALE) # read in the image as grayscale
    imgnew = img
    print(img.shape)
    xmin = 0
    #xmax = shape.

    xmiddle = int((xmax - xmin)/2)
    imgnew, paramList = scanImage(0, xmiddle)
    #meanPhase, stdPhase, phases, paramListRight = scanImage(xmiddle, xmax)

    filenameNoExt, file_extension = os.path.splitext(archivoProcesar)
    outputPath = os.path.join(filenameNoExt + "_equalized" + file_extension)
    cv2.imwrite(outputPath, imgnew)


