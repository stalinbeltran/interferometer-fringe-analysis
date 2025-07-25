#python equalizeImage.py ./images/alineacion666_rescaled.png 250

import globals
import numpy as np
import cv2
import os
from scipy.optimize import curve_fit

def isBlackImage(img):
    mean = np.mean(img)
    if mean > globals.BLACK_IMAGE_LEVEL:
        print(mean)
        return False
    return True

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
  
def verticalSineFit(img, guessedWavelength):
    guessedParameters = {
        "guessedAmplitude": 125,
        "guessedWavelength": guessedWavelength,
        "guessedPhase": 0.5,
        "guessedVerticalDisplacement": 0
    }
    guessedAmplitude = guessedParameters["guessedAmplitude"]
    guessedWavelength = guessedParameters["guessedWavelength"]
    guessedPhase = guessedParameters["guessedPhase"]
    guessedVerticalDisplacement = guessedParameters["guessedVerticalDisplacement"]    
    initial_guess = [guessedAmplitude, 2*np.pi/guessedWavelength, guessedPhase, guessedVerticalDisplacement]
    
    slc = img[:, 0]             #our image has the same vertical wave (if equalized)

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

    return fittedParameters

def getHorizontalMean(img):
    ymin = 0
    height, width = img.shape
    ymax = height     #width of the image
    imgnew = np.empty((height, 10), dtype=np.uint8)
    for row in range(ymin, ymax):
        rowMean = np.mean(img[row])
        imgnew[row, :] = int(rowMean)
    return imgnew
