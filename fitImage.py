#D:\Stalin\Desarrollo\interferometer-fringe-analysis>python fitImage.py ./videos/fringes_7/framesRescaled ./videos/fringes_7/framesFitImage ./videos/fringes_7/framesFitImagejson 300

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys
import os
import imageSineFit as isf
import json

input_folder = (sys.argv[1])
output_folder = (sys.argv[2])
outputJSON_folder = (sys.argv[3])
guessedWavelength = float(sys.argv[4])
os.makedirs(output_folder, exist_ok=True)
os.makedirs(outputJSON_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        outputPath = os.path.join(output_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        filenameJSON = filenameNoExt + ".json"
        outputPathJSON = os.path.join(outputJSON_folder, filenameJSON)
        imageSineFit = isf.imageSineFit(inputPath, outputPath, guessedWavelength)
        outputJSON_folder
        with open(outputPathJSON, 'w') as f:
            json.dump(imageSineFit, f)
        print(outputPath, outputPathJSON)




