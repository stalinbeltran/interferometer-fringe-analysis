#python3 getNoise.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseSoften.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-Noise.json


import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getNoise(key, originalData, softData):
    size = len(originalData)
    noises = []
    for i in range(size):
        original = originalData[i]
        soft = softData[i]
        dif = original-soft
        noises.append(dif)
    return noises
    
def getNoiseByKey(N, originalData, softData):
    noiseData = {}
    for key in ["fixedPhase", "mobilePhase", "hz"]:
        noise = getNoise(key, originalData[key], softData["data"][key])
        noiseData[key] = noise
    return {
        "N" : N,
        "data" : noiseData
    }
    
'''
			"data":{
					{"fixedPhase": [1, 2, 3, 4...],
					 "mobilePhase": [1, 2, 3, 4...],
					 "hz": [1, 2, 3, 4...]
					}
			}
'''
            
            
with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

originalData = dataJSON["original"]["data"]
softenedArray = dataJSON["softened"]
noises = []
for softData in softenedArray:
    noise = getNoiseByKey(softData["N"], originalData, softData)
    noises.append(noise)
    
outputJSON = {
	"noises": noises
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)


'''
set de noisees original-suavizada N (imprimir datos, y elegir los menores noisees obtenidos):

{
	"noises":[
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