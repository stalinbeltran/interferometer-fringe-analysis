#python3 blurImages.py ./videos/fringes_65/frames ./videos/fringes_65/framesSoftened

import numpy as np
import cv2
import os
import sys

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
            print('magnitude: ', absftFlat[i]/1000000)
            print('phase: ', phase)
            print('periodo: ', period)
            break
    


input_folder = (sys.argv[1])
c = 0
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png')):
        inputPath = os.path.join(input_folder, filename)
        image = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        getParameters(image)
        print("\n")
        c+=1
    if c > 20:  break
    
cv2.destroyAllWindows()
