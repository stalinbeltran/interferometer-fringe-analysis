#python3 getDeltaPhase.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseSoften.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-DeltaPhase.json 


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


def getDeltaPhase(softData):
    dataMobile = softData["mobilePhase"]
    dataFixed = softData["fixedPhase"]
    deltaPhase = [dataMobile[i] - dataFixed[i] for i in range(len(dataMobile))]
    return deltaPhase

  

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

softenedArray = dataJSON
for softData in softenedArray:
    print(softData["N"])
    deltaPhase = getDeltaPhase(softData["data"])
    softData["data"]["deltaPhase"] = deltaPhase



with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSON, f, ensure_ascii=False, indent=4)
