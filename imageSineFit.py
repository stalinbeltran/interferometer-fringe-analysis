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
        guessedAmplitude = guessedParameters["guessedAmplitude"]
        guessedWavelength = guessedParameters["guessedWavelength"]
        guessedPhase = guessedParameters["guessedPhase"]
        guessedVerticalDisplacement = guessedParameters["guessedVerticalDisplacement"]
        
        initial_guess = [guessedAmplitude, 2*np.pi/guessedWavelength, guessedPhase, guessedVerticalDisplacement]
        len = np.size(slc)
        x = range(0, len)
        # Perform the curve fitting
        try:
            params, covariance = curve_fit(sine_function, x, slc, p0=initial_guess)
        except Exception as e:
            print('Error', e)
            continue    #if no fit, left slice unchanged, no fit getted
            
        paramsList.append(params)
        A_fit, B_fit, C_fit, D_fit = params     # Extract the fitted parameters
        y_fit = sine_function(x, A_fit, B_fit, C_fit, D_fit)    # Generate y values using the fitted parameters
        imgnew[:, int(target_slice)] = y_fit            #modify image with the best fit found
        
    return imgnew, paramsList 
  
def imageEqualize(archivoProcesar, guessedWavelength):
    img = cv2.imread(archivoProcesar, cv2.IMREAD_GRAYSCALE) # read in the image as grayscale
    imgnew = img
    xmin = 0
    xmax = img.shape[1]     #width of the image
    guessedParameters = {
        "guessedAmplitude": 250,
        "guessedWavelength": guessedWavelength,
        "guessedPhase": 0.5,
        "guessedVerticalDisplacement": 0
    }
    xmiddle = int((xmax - xmin)/2)
    imgnew, paramList = scanImage(img, 0, xmiddle, guessedParameters, imgnew)
    #meanPhase, stdPhase, phases, paramListRight = scanImage(xmiddle, xmax)

    filenameNoExt, file_extension = os.path.splitext(archivoProcesar)
    outputPath = os.path.join(filenameNoExt + "_equalized" + file_extension)
    cv2.imwrite(outputPath, imgnew)
    return outputPath, paramList

