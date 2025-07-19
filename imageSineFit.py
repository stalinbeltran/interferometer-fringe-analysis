#python equalizeImage.py ./images/alineacion666_rescaled.png 250

import numpy as np
import cv2
import os
from scipy.optimize import curve_fit

def isBlackImage(img):
    return np.mean(img) < 60

def sine_function(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

def scanImage(img, guessedParameters, imgnew):
    paramsList = []
    # Initial guess for the parameters [A, B, C, D]
    guessedAmplitude = guessedParameters["guessedAmplitude"]
    guessedWavelength = guessedParameters["guessedWavelength"]
    guessedPhase = guessedParameters["guessedPhase"]
    guessedVerticalDisplacement = guessedParameters["guessedVerticalDisplacement"]    
    initial_guess = [guessedAmplitude, 2*np.pi/guessedWavelength, guessedPhase, guessedVerticalDisplacement]
    
    xmin = 0
    xmax = img.shape[1]     #width of the image
    for target_slice in range(xmin, xmax):
        slc = img[:, int(target_slice)]             #take a slice to process

        len = np.size(slc)
        x = range(0, len)
        # Perform the curve fitting
        try:
            params, covariance = curve_fit(sine_function, x, slc, p0=initial_guess)
            perr = np.sqrt(np.diag(covariance))
            fittedParameters = {
                "amplitude":{
                    "value": params[0],
                    "error": perr[0]
                },
                "frequency":{
                    "value": params[1],
                    "error": perr[1]
                },
                "phase":{
                    "value": params[2],
                    "error": perr[2]
                },
                "verticalDisplacement":{
                    "value": params[3],
                    "error": perr[3]
                }
            }
        except Exception as e:
            print('Error', e)
            continue    #if no fit, left slice unchanged, no fit getted
            
        paramsList.append(fittedParameters)
        A_fit, B_fit, C_fit, D_fit = params     # Extract the fitted parameters
        y_fit = sine_function(x, A_fit, B_fit, C_fit, D_fit)    # Generate y values using the fitted parameters
        imgnew[:, int(target_slice)] = y_fit            #modify image with the best fit found

    return imgnew, paramsList 
  
def imageSineFit(inputFile, outputFile, guessedWavelength):
    img = cv2.imread(inputFile, cv2.IMREAD_GRAYSCALE) # read in the image as grayscale
    print(img)
    imgnew = img

    guessedParameters = {
        "guessedAmplitude": 250,
        "guessedWavelength": guessedWavelength,
        "guessedPhase": 0.5,
        "guessedVerticalDisplacement": 0
    }
    imgnew, paramList = scanImage(img, guessedParameters, imgnew)
    print('imgnew')
    print(imgnew)
    cv2.imwrite(outputFile, imgnew)
    imageSineFit = {
        "imagepath": {
            "input": inputFile, 
            "output": outputFile
        },
        "fitParameters": paramList

    }
    return imageSineFit

def scanImageMean(img, imgnew):
    ymin = 0
    ymax = img.shape[0]     #width of the image
    imgnew = img
    for row in range(ymin, ymax):
        rowMean = np.mean(img[row])
        imgnew[row, :] = rowMean
    return imgnew