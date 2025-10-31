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
    totalData = []
    segments = segmentsJSON["segments"]
    for segment in segments:
        samples = segment["samples"]
        data = getData(samples, key)
        totalData.extend(data)
    return totalData

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
timestamp = getPlainData(segmentsJSON, "timestamp")
mobilePhase = getPlainData(segmentsJSON, "mobilePhase")
fixedPhase = getPlainData(segmentsJSON, "fixedPhase")
hz = getPlainData(segmentsJSON, "hz")
deltaPhase = getPlainData(segmentsJSON, "deltaPhase")

jsonData = [
    {
        "data": globals.getData(fixedPhase, mobilePhase, hz, timestamp, deltaPhase)
    }
]

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(jsonData, f, ensure_ascii=False, indent=4)


print("ended")