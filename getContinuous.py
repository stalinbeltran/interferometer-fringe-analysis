#python3 getContinuous.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseSoften.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-Continuous.json


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
parameters = (sys.argv[3])

parts = parameters.split(':')
begin = int(parts[0])
end = int(parts[1])
step = int(parts[2])

    
def getSoftenedData(N, fixedPhase, mobilePhase, hz, timestamp):
    return {
        "N" : N,
        "data" : globals.getData(fixedPhase, mobilePhase, hz, timestamp)
    }
    

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

timestamp = dataJSON[0]["data"]["timestamp"]
fixedPhase = dataJSON[0]["data"]["fixedPhase"]
mobilePhase = dataJSON[0]["data"]["mobilePhase"]
hz = dataJSON[0]["data"]["hz"]


originalData = {
    "data": globals.getData(fixedPhase, mobilePhase, hz, timestamp)
}

softened = []
softened.append(getSoftenedData(0, fixedPhase, mobilePhase, hz, timestamp))
for N in range(begin, end, step):
    fixedPhase = globals.softenSignal(originalData["data"]["fixedPhase"], N)
    mobilePhase = globals.softenSignal(originalData["data"]["mobilePhase"], N)
    hz = globals.softenSignal(originalData["data"]["hz"], N)
    softened.append(getSoftenedData(N, fixedPhase, mobilePhase, hz, timestamp))



outputJSON = softened

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)





