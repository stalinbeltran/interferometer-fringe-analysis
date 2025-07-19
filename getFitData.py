#python3 getFitData.py ./videos/fringes_44/framesLeftEqualized 120

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys
import os
import imageSineFit as isf
import json

input_folder = (sys.argv[1])
guessedWavelength = float(sys.argv[2])

fitDataList = []
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        img = cv2.imread(inputPath, 0)
        fitData = isf.verticalSineFit(img, guessedWavelength)
        fitDataList.append(fitData)
        break
outputPath = os.path.join(input_folder, "fitData.json")
with open(outputPath, 'w') as f:
    json.dump(fitDataList, f)
print(outputPath)