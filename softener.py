#python3 softener.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PlainData.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseSoften.json 3:10:2


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

    
def getSoftenedData(N, fixedPhase, mobilePhase, hz, timestamp, deltaPhase):
    return {
        "N" : N,
        "data" : globals.getData(fixedPhase, mobilePhase, hz, timestamp, deltaPhase)
    }
    

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

timestamp = dataJSON[0]["data"]["timestamp"]
fixedPhase = dataJSON[0]["data"]["fixedPhase"]
mobilePhase = dataJSON[0]["data"]["mobilePhase"]
deltaPhase = None
if deltaPhase in dataJSON[0]["data"]:
    deltaPhase = dataJSON[0]["data"]["deltaPhase"]
hz = dataJSON[0]["data"]["hz"]


originalData = {
    "data": globals.getData(fixedPhase, mobilePhase, hz, timestamp, deltaPhase)
}

softened = []
softened.append(getSoftenedData(0, fixedPhase, mobilePhase, hz, timestamp, deltaPhase))
for N in range(begin, end, step):
    fixedPhase = globals.softenSignal(originalData["data"]["fixedPhase"], N)
    mobilePhase = globals.softenSignal(originalData["data"]["mobilePhase"], N)
    deltaPhase = None
    if deltaPhase in originalData["data"]:
        deltaPhase = globals.softenSignal(originalData["data"]["deltaPhase"], N)
    hz = globals.softenSignal(originalData["data"]["hz"], N)
    softened.append(getSoftenedData(N, fixedPhase, mobilePhase, hz, timestamp, deltaPhase))



outputJSON = softened

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)





