#python3 getPlainData.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PhaseUnwrapped.json D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PlainData.json


import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getData(samples, key):
    data = [ sample[key] for sample in samples]
    return data
    

def getPlainData(segmentsJSON, key):
    segments = segmentsJSON["segments"]
    processed = 0
    for segment in segments:
        samples = segment["samples"]
        data = getData(samples, key)
        segment[key] = data
        processed+=1

    print("processed: ", processed)

def deleteSamples(segmentsJSON):
    segments = segmentsJSON["segments"]
    processed = 0
    for segment in segments:
        del segment["samples"]
        processed+=1

    print("processed: ", processed)

def getTimestampsValues(segmentsJSON):
    segments = segmentsJSON["segments"]
    processed = 0
    for segment in segments:
        samples = segment["samples"]
        for sample in samples:
            timestamp = float(sample["timestamp"])
            sample["timestamp"] = timestamp
            processed+=1

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

getTimestampsValues(segmentsJSON)
getPlainData(segmentsJSON, "timestamp")
getPlainData(segmentsJSON, "mobilePhase")
getPlainData(segmentsJSON, "fixedPhase")
getPlainData(segmentsJSON, "hz")
deleteSamples(segmentsJSON)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

