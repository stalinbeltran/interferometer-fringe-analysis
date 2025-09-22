 #python3 getFFT.py ./60hzSegmentSamples.json ./60hzSegmentSamplesFFT.json

import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getFFTParameters(imagePath):
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    sizex = image.shape[1]        #number of columns
    ft = np.fft.ifftshift(image)
    ft = np.fft.fft2(ft)
    sample_spacing_x = 1
    freq_x = np.fft.fftfreq(sizex, d=sample_spacing_x)
    absft = abs(ft)
    absftFlat = absft.flatten()
    sorted_indices = np.argsort(-absftFlat)
    
    magnitude = None
    phase = None
    period = None
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
            break
    fftParams = {"magnitude":magnitude, "phase":phase, "period":period, }
    return fftParams


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]

for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        fileMobile["fftParams"] = getFFTParameters(fileMobile["absolutePath"])
        fileFixed["fftParams"] = getFFTParameters(fileFixed["absolutePath"])


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

