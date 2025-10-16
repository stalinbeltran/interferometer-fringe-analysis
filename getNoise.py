#python3 getErrors.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseSoften.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-Errors.json


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

def getError(key, originalData, softData):
    size = len(originalData)
    errors = []
    for i in range(size):
        original = originalData[i]
        soft = softData[i]
        dif = original-soft
        errors.append(dif)
    return errors
    
def getErrorByKey(N, originalData, softData):
    errorData = {}
    for key in ["fixedPhase", "mobilePhase", "hz"]:
        error = getError(key, originalData[key], softData["data"][key])
        errorData[key] = error
    return {
        "N" : N,
        "data" : errorData
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
errors = []
for softData in softenedArray:
    error = getErrorByKey(softData["N"], originalData, softData)
    errors.append(error)
    
outputJSON = {
	"errors": errors
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)


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