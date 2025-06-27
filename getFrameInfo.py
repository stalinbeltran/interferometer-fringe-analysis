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
os.makedirs(output_folder, exist_ok=True)

        outputPath = os.path.join(output_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        filenameJSON = filenameNoExt + ".json"
        outputPathJSON = os.path.join(outputJSON_folder, filenameJSON)
        
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        with open(inputPath, 'r') as f:
            data = json.load(f)
        print('data', data)
    break
'''
    imageSineFit = {
        "imagepath": {
            "input": inputFile, 
            "output": outputFile
        },
        "fitData":{
            "leftSide": {
                "fitParameters": paramListLeft
            },
            "rightSide": {
                "fitParameters": paramListRight
            },
        }

    }
	
    '''