#python3 softener.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseUnwrapped.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseSoften.json 40


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])

begin = 3
end = 20
step = 3

def getData(fixedPhase, mobilePhase, hz):
    return {
        "fixedPhase" : fixedPhase,
        "mobilePhase" : mobilePhase,
        "hz" : hz
    }
    
def getSoftenedData(N, fixedPhase, mobilePhase, hz):
    return {
        "N" : N,
        "data" : getData(fixedPhase, mobilePhase, hz)
    }
    

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

fixedPhase = dataJSON["fixedPhase"]
mobilePhase = dataJSON["mobilePhase"]
hz = dataJSON["hz"]


originalData = {
    "data": getData(fixedPhase, mobilePhase, hz)
}

softened = []
for N in range(begin, end, step):
    fixedPhase = globals.softenSignal(originalData["data"]["fixedPhase"], N)
    mobilePhase = globals.softenSignal(originalData["data"]["mobilePhase"], N)
    hz = globals.softenSignal(originalData["data"]["hz"], N)
    softened.append(getSoftenedData(N, fixedPhase, mobilePhase, hz))



outputJSON = {
    "original" : originalData,
    "softened" : softened
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)


'''
sets data original y suavizada:

{
	"original":
		{
			"data":{
					{"fixedPhase": [1, 2, 3, 4...],
					 "mobilePhase": [1, 2, 3, 4...],
					 "hz": [1, 2, 3, 4...]
					}
			}
		},
	"softened":[
		{
			"N": 4,
			"data":{
					"fixedPhase": [1, 2, 3, 4...],
					 "mobilePhase": [1, 2, 3, 4...],
					 "hz": [1, 2, 3, 4...]
					
			}
		},
		
		{
			"N": 8,
			"data":{
					{"fixedPhase": [],
					 "mobilePhase": [],
					 "hz": []
					}
			}
		}
	]

}
'''



