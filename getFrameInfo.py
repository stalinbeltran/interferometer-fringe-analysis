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
#os.makedirs(output_folder, exist_ok=True)

outputPath = os.path.join(output_folder, 'frames.json')

for filename in os.listdir(input_folder):
    inputPath = os.path.join(input_folder, filename)
    with open(inputPath, 'r') as f:
        data = json.load(f)
    # print('data', data)
    # print(data.keys())
    #dict_keys(['imagepath', 'fitData'])
    fitData = data["fitData"]
    #print(fitData.keys())
    #dict_keys(['leftSide', 'rightSide'])
    leftData = fitData["leftSide"]
    #print(leftData.keys())
    #dict_keys(['fitParameters'])
    parameters = leftData["fitParameters"]
    #print(parameters[0])
    #{'amplitude': {'value': 52.445338132835005, 'error': 1.5758581058845498}, 'wavelength': {'value': 0.012312298713821406, 'error': 9.062006024708478e-05}, 'phase': {'value': 5.493020119917932, 'error': 0.055429869589786004}, 'verticalDisplacement': {'value': 105.12554035537349, 'error': 1.1043501120158479}}
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