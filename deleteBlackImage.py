#python3 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/deleteBlackImage.py /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_40/frames
#python /home/stalin/interferometer-fringe-analysis/deleteBlackImage.py /home/stalin/interferometer-fringe-analysis/videos/fringes_45/frames

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import sys
import os
import imageSineFit as isf
import json
import numpy as np

input_folder = (sys.argv[1])

imgf = None
c = 0
for filename in os.listdir(input_folder):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    inputPath = os.path.join(input_folder, filename)
    img = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE) # read in the image as grayscale
    if isf.isBlackImage(img):
        os.remove(inputPath)        #delete black images
    else: print(filename + " mean: " + str(np.mean(img)))
    
