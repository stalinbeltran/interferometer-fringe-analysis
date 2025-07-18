#python3 compareImages.py ./videos/fringes_65/frames/ ./videos/fringes_65/frames/fringes_65-483-.png 25505474

import numpy as np
import cv2
import os
import sys
import imageSineFit as isf

input_folder = (sys.argv[1])
dim = 25
product = dim*dim

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        img1 = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        kernel = np.ones((dim,dim),np.float32)/product
        imgBlurred = cv2.filter2D(img1,-1,kernel)
        #outputPath = os.path.join(input_folder, filenameNoExt + "-blurred" + file_extension)
        outputPath = inputPath
        cv2.imwrite(outputPath, imgBlurred)
cv2.destroyAllWindows()