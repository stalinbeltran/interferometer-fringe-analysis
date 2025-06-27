#python equalizeImage.py ./images/alineacion666_rescaled.png 250

import numpy as np
import cv2
import os
from scipy.optimize import curve_fit

def isBlackImage(img):
    return np.mean(img) < 90

def sine_function(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

def findGivenParamMean(paramName, paramsList):
    size = len(paramsList)
    values = np.empty(size)
    i = 0
    for params in paramsList:
        # if params[paramName]["error"] < 1:
        values[i] = params[paramName]["value"]
        i +=1
    
    mean = np.mean(values)
    return mean

def getBetterGuessedParameters(paramsList):
    #for params in paramsList:
        #print(params)
        # if params["amplitude"]["error"] < 0.1:
            # amplitudes.append(
        #break
    guessedParameters = {
        "guessedAmplitude": findGivenParamMean("amplitude", paramsList),
        "guessedWavelength": 2*np.pi*findGivenParamMean("wavelength", paramsList),
        "guessedPhase": findGivenParamMean("phase", paramsList),
        "guessedVerticalDisplacement": findGivenParamMean("verticalDisplacement", paramsList)
    }
    return guessedParameters
        
def scanImageRange(img, xbegin, xend, guessedParameters, imgnew):
    paramsList = []
    counter = 0
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
            perr = np.sqrt(np.diag(covariance))
            fittedParameters = {
                "amplitude":{
                    "value": params[0],
                    "error": perr[0]
                },
                "wavelength":{
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
        #print(fittedParameters)
        paramsList.append(fittedParameters)
        A_fit, B_fit, C_fit, D_fit = params     # Extract the fitted parameters
        y_fit = sine_function(x, A_fit, B_fit, C_fit, D_fit)    # Generate y values using the fitted parameters
        imgnew[:, int(target_slice)] = y_fit            #modify image with the best fit found
        counter+=1
        if counter % 20 == 0:
            guessedParameters = getBetterGuessedParameters(paramsList)
           

    return imgnew, paramsList 
  
def imageSineFit(inputFile, outputFile, guessedWavelength):
    img = cv2.imread(inputFile, cv2.IMREAD_GRAYSCALE) # read in the image as grayscale
    if isBlackImage(img):
        return None
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
    imgnew, paramListLeft = scanImageRange(img, 0, xmiddle, guessedParameters, imgnew)
    imgnew, paramListRight = scanImageRange(img, xmiddle, xmax, guessedParameters, imgnew)

    cv2.imwrite(outputFile, imgnew)
    imageSineFit = {
        "imagepath": {
            "input": inputFile, 
            "output": outputFile
        },
        "fitData":{
            "leftSide": {
                "fitParameters": paramListLeft
            },
            "rightSide": {
                "fitParameters": paramListRight
            },
        }

    }
    return imageSineFit

