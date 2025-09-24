#python3 getFFT.py ./60hzSegmentSamples.json ./60hzSegmentSamplesFFT.json
#python3 getFFT.py ./40hzSegmentSamples.json ./40hzSegmentSamplesFFT.json
#python3 getFFT.py ./60hzSegmentSamplesFFT.json ./60hzSegmentSamplesFFT.json
#python3 getFFT.py ./40hzSegmentSamplesFFT.json ./40hzSegmentSamplesFFT.json

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
    for i in range(0, 60):
        period = sizex
        maxPosition = sorted_indices[i]
        index = np.unravel_index(maxPosition, np.shape(ft))
        frequency = freq_x[index[1]]
        if frequency > 0: period = 1/frequency
        if frequency > 0 and period < sizex/4:      #we expect at least 4 wavelengths in each image
            imaginaryValue = ft[index]
            phase = np.angle(imaginaryValue, True)
            magnitude = absftFlat[i]/1000000
            break
    fftParams = {"magnitude":magnitude, "phase":phase, "period":period, }
    return fftParams


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        if "fftParams" not in fileMobile or "magnitude" in fileMobile["fftParams"] and fileMobile["fftParams"]["magnitude"] is None:
            fileMobile["fftParams"] = getFFTParameters(fileMobile["absolutePath"])
            #print(fileMobile["absolutePath"])
            processed+=1

        if "fftParams" not in fileFixed or "magnitude" in fileFixed["fftParams"] and fileFixed["fftParams"]["magnitude"] is None:
            fileFixed["fftParams"] = getFFTParameters(fileFixed["absolutePath"])
            #print(fileFixed["absolutePath"])
            processed+=1
        #if processed > 1: break
print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

