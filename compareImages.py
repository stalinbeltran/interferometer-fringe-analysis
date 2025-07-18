#python3 compareImages.py ./videos/fringes_65/frames/ ./videos/fringes_65/frames/fringes_65-483-.png 25505474

import numpy as np
import cv2
import os
import sys
import imageSineFit as isf

input_folder = (sys.argv[1])
img0_path = (sys.argv[2])
threshold = float(sys.argv[3])

img0 = cv2.imread(img0_path, cv2.IMREAD_GRAYSCALE)
img0 = 1.0*img0/255
maxDiff = 640*480.0

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        img1 = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        img1 = 1.0*img1/255
        diff = np.absolute(img0-img1)
        difference = np.sum(diff)/maxDiff
        if difference == 0: continue        #in case of the exactly same image
        if difference < threshold:
            print("archivo: ", filename, " - ", difference)

cv2.destroyAllWindows()