#python3 sectionSoftener.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-HzSections.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-HzSectionsSoftened.json

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

input_file = (sys.argv[1])
output_file = (sys.argv[2])
N = globals.getPromptOptionalParameter(3, int)


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

for section in dataJSON:
    data = section["data"]
    deltaPhase = data["original"]["deltaPhase"]
    hz = data["original"]["hz"]
    deltaPhase = globals.softenSignal(deltaPhase, N)
    hz = globals.softenSignal(hz, N)
    data["softened_" + str(N)] = {"deltaPhase":deltaPhase , "hz":hz}           #deltaPhase

outputJSON = dataJSON

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(outputJSON, f, ensure_ascii=False, indent=4)

