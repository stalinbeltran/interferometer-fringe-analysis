#python3 compareImages.py ./videos/fringes_65/frames/ ./videos/fringes_65/frames/fringes_65-1-.png 30000

import numpy as np
import cv2
import os
import sys
import imageSineFit as isf

input_folder = (sys.argv[1])
img0_path = (sys.argv[2])
threshold = float(sys.argv[3])

img0 = cv2.imread(img0_path, cv2.IMREAD_GRAYSCALE)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        img1 = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        if isf.isBlackImage(img1):
            continue                #ignore black images
        diff = np.absolute(img0-img1)
        
        print(img0)
        print(img1)
        difference = np.sum(diff)
        print(diff)
        cv2.imshow('frame', diff)
        break
        print("archivo: ", filename, " - ", difference)
        if difference < threshold:
            print("archivo: ", filename, " - ", difference)
            break
            

cv2.waitKey()

cv2.destroyAllWindows()