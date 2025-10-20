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
    for key in ["fixedPhase", "mobilePhase", "hz", "deltaPhase"]:
        noise = getNoise(key, originalData[key], softData["data"][key])
        noiseData[key] = noise
    return {
        "N" : N,
        "data" : noiseData
    }
    

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

originalData = dataJSON[0]["data"]          #first element is the original (unmodified) data
softenedArray = dataJSON
noises = []
for softData in softenedArray:
    N = 0
    if "N" in softData:
        N = softData["N"]
    if N == 0: continue                     #no noise for the original data
    noise = getNoiseByKey(N, originalData, softData)
    noises.append(noise)
    
outputJSON = noises


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)
