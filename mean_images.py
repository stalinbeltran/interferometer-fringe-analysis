#python mean_images.py ./videos/fringes_9/framesCropped

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
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
    if imgf is None:
        imgf = img.astype(np.float32)
    else:
        imgf += img
    #if c == 20: break
    c+=1
    
imgf /= 1.0*c
print(img[0:4, 0:2])
print(imgf[0:4, 0:2])
imgMean = imgf.astype(np.uint8)
print(np.max(imgMean))
cv2.imshow('image', imgMean)
cv2.waitKey(0)


for filename in os.listdir(input_folder):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    inputPath = os.path.join(input_folder, filename)
    img = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE) # read in the image as grayscale
    img = img.astype(np.float32)
    img -= imgf
    img /=2.0
    
    img = img.astype(np.uint8)
    if c == 10: break
    c+=1
    cv2.imshow('image', img)
    cv2.waitKey(0)