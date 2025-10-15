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
N_points = int(sys.argv[3])

def getData(samples, key):
    data = [ sample[key] for sample in samples]
    return data
    

def softenSignal(segmentsJSON, key):
    global N_points

    kernel = np.ones(N_points) / N_points           #averaging kernel
    segments = segmentsJSON["segments"]
    processed = 0
    for segment in segments:
        samples = segment["samples"]
        data = getData(samples, key)
        if len(data)==0: continue
        convolution = np.convolve(data, kernel, mode='same')
        segment[key] = convolution.tolist()
        processed+=1

    print("processed: ", processed)



with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

softenSignal(segmentsJSON, "mobilePhase")
softenSignal(segmentsJSON, "fixedPhase")
softenSignal(segmentsJSON, "hz")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

