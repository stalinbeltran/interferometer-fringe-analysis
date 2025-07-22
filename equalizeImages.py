#python3 equalizeImages.py ./videos/fringes_44/framesLeft ./videos/fringes_44/framesLeftEqualized

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys
import os
import imageSineFit as isf

input_folder = (sys.argv[1])
output_folder = (sys.argv[2])
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        outputPath = os.path.join(output_folder, filename)
        img = cv2.imread(inputPath, 0)
        imgnew = isf.getHorizontalMean(img, img)
        cv2.imwrite(outputPath, imgnew)
        #break