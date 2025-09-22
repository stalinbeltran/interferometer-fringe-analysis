 #python3 getSamples.py ./60hzSegments.json ./60hzSegmentSamples.json

import os
import sys
import json

input_file = (sys.argv[1])
output_file = (sys.argv[2])

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


with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
segmentsNew = []

for segment in segments:
    files = segment["files"]
    t = float(files[2]["timestamp"]) - float(files[0]["timestamp"])
    for file in files:
        timestamp = file["timestamp"]


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

