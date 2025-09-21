#python3 imageProcessing.py ./videos/fringes_65/frames ./videos/fringes_65/framesSoftened

import numpy as np
import cv2
import os
import sys
from datetime import datetime

def getParameters(image):
    sizex = image.shape[1]        #number of columns
    ft = np.fft.ifftshift(image)
    ft = np.fft.fft2(ft)
    sample_spacing_x = 1
    freq_x = np.fft.fftfreq(sizex, d=sample_spacing_x)
    absft = abs(ft)
    absftFlat = absft.flatten()
    sorted_indices = np.argsort(-absftFlat)

    for i in range(0, 6):
        period = sizex
        maxPosition = sorted_indices[i]
        index = np.unravel_index(maxPosition, np.shape(ft))
        frequency = freq_x[index[1]]
        if frequency > 0: period = 1/frequency
        if frequency > 0 and period < sizex/2:
            imaginaryValue = ft[index]
            phase = np.angle(imaginaryValue, True)
            magnitude = absftFlat[i]/1000000
            print('magnitude: ', magnitude)
            print('phase: ', phase)
            print('periodo: ', period)
            break
    return magnitude, phase, period


input_folder = (sys.argv[1])
c = 0
timestampBefore = 0
difBefore = 0
fixedMirrorFile = ""
mobileMirrorFile = ""
lastFile = None
dif = 0
HIGHER_LIMIT = 1/6.666

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png')):
        parts = filename.split('-')
        timestamp = float(parts[1])
        if timestampBefore > 0:
            dif = timestamp - timestampBefore
        if dif > HIGHER_LIMIT:
            print('gap')
            difBefore = 0               #temporal gap here (beginning of a new set)
            lastFile = filename
            timestampBefore = timestamp
            continue                    #this file is the first, check the next one
            
        if dif > difBefore:                 #mobile mirror
            mobileMirrorFile = filename
            
        if dif < difBefore:                 #fixed mirror
            fixedMirrorFile = filename
        
        lastFile = filename
        difBefore = dif
        timestampBefore = timestamp
        if mobileMirrorFile and fixedMirrorFile:
            inputPath_mobileMirrorFile = os.path.join(input_folder, mobileMirrorFile)
            imageMobileMirror = cv2.imread(inputPath_mobileMirrorFile, cv2.IMREAD_GRAYSCALE)
            magnitude, phase, period = getParameters(imageMobileMirror)
            mobileMirror = {
                "magnitude" : magnitude, 
                "phase" : phase, 
                "period" : period, 
            }
            inputPath_fixedMirrorFile = os.path.join(input_folder, fixedMirrorFile)
            imageFixedMirror = cv2.imread(inputPath_fixedMirrorFile, cv2.IMREAD_GRAYSCALE)
            magnitude, phase, period = getParameters(imageFixedMirror)
            fixedMirror = {
                "magnitude" : magnitude, 
                "phase" : phase, 
                "period" : period, 
            }
            
            print(mobileMirror, fixedMirror, "\n")
            mobileMirrorFile = None
            fixedMirrorFile = None
            c+=1
    if c > 0:  break
    
cv2.destroyAllWindows()
