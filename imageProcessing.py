#python3 blurImages.py ./videos/fringes_65/frames ./videos/fringes_65/framesSoftened

import numpy as np
import cv2
import os
import sys

def getParameters(image):
    sizex = image.shape[1]        #number of columns
    print(sizex)
    ft = np.fft.ifftshift(image)
    ft = np.fft.fft2(ft)
    sample_spacing_x = 1
    freq_x = np.fft.fftfreq(sizex, d=sample_spacing_x)
    absft = abs(ft)
    absftFlat = absft.flatten()
    sorted_indices = np.argsort(-absftFlat)

    for i in range(0, 6):
        maxPosition = sorted_indices[i]
        print("maxPosition: " + str(maxPosition))
        index = np.unravel_index(maxPosition, np.shape(ft))
        if freq_x[index[1]] > 0:        
            imaginaryValue = ft[index]
            maxAngle = np.angle(imaginaryValue, True)
            print('magnitude: ', absftFlat[i]/1000000)
            print('maxAngle: ', maxAngle)
            print('periodo: ', 1/freq_x[index[1]])
        print("\n")
    


input_folder = (sys.argv[1])

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png')):
        inputPath = os.path.join(input_folder, filename)
        image = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        getParameters(image)
    break
cv2.destroyAllWindows()
