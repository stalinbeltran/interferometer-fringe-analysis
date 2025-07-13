
import numpy as np
import cv2
import os
import sys
import imageSineFit as isf

input_folder = (sys.argv[1])
img0_path = (sys.argv[2])
threshold = float(sys.argv[3])

img0 = cv2.imread(img0_path, cv2.IMREAD_GRAYSCALE)
img0_norm = img0/np.sum(img0)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        img1 = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        if isf.isBlackImage(img1):
            continue                #ignore black images

        img1_norm = img1/np.sum(img1)
        similarity = np.sum(np.sqrt(img0_norm*img1_norm))
        if similarity > threshold:
            print("archivo: ", filename, " - ", similarity)


cv2.destroyAllWindows()