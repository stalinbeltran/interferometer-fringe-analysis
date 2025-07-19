#python3 blurImages.py ./videos/fringes_65/frames ./videos/fringes_65/framesSoftened03

import numpy as np
import cv2
import os
import file
import sys
import imageSineFit as isf
import blurImage as blur

input_folder = (sys.argv[1])
output_folder = (sys.argv[2])
file.createDirectory(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        img1 = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        imgBlurred = blur.blurImage(img1)
        outputPath = os.path.join(output_folder, filenameNoExt + "" + file_extension)
        cv2.imwrite(outputPath, imgBlurred)
        # cv2.imshow('-', imgBlurred)
        # cv2.waitKey()
        # break
cv2.destroyAllWindows()