#python3 showHistogram.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PlainData.json mobilePhase


import os
import sys
import json
import cv2
import numpy as np
import histogram
import globals
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
key = (sys.argv[2])
histogramRange = (0,0)
if len(sys.argv)>3:
    histogramRange = (sys.argv[3])
    histogramRange = histogramRange.split(':')


#showHistogram(data, title='-', bins=30, show = True, label = None, histtype='bar', stacked = False)

def showFileData(input_file, key, histogramRange):
    global sampleSize
    path, filename = globals.getFileName(input_file)
    with open(input_file, 'r', encoding='utf-8') as f:
        dataJSON = json.load(f)

    title = input_file
    for data in dataJSON:
        label = key + " N = " + str(data["N"])
        histogram.showHistogram(data["data"][key], title, label = [label], histogramRange = histogramRange)


showFileData(input_file, key, histogramRange)

'''

set de errores original-suavizada N (imprimir datos, y elegir los menores errores obtenidos):

{
	"errors":[
		{
			"N": 4,
			"mean": 0.2,
			"std": 3.2,
			"data":{
				
				 "fixedPhase": [1, 2, 3, 4...],
				 "mobilePhase": [1, 2, 3, 4...],
				 "hz": [1, 2, 3, 4...]
				
			}
		},
	
	]
}


'''