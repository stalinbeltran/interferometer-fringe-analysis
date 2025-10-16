#python3 diff.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PlainData.json  


import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file1 = (sys.argv[1])
input_file2 = (sys.argv[2])
key = (sys.argv[3])
output_file = (sys.argv[4])

#showHistogram(data, title='-', bins=30, show = True, label = None, histtype='bar', stacked = False)

def getData(input_file, key):
    global sampleSize
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    data = []
    segments = segmentsJSON["segments"]
    for segment in segments:
        data.append(segment[key])
    return data

data1 = getData(input_file1, key)
data2 = getData(input_file2, key)
size = len(data1)
size2 = len(data2)
if size != size2:
    print()
    exit("different segments length")
    
segments = []
for i in range(0, size):
    segment1 = data1[i]
    segment2 = data2[i]
    listSize = len(segment1)
    listSize2 = len(segment2)
    if listSize != listSize2:
        exit("different data length")
        exit()
    dataOut = []
    for j in range(0, listSize):
        d1 = segment1[j]
        d2 = segment2[j]
        dataOut.append(abs(d1 - d2))
    
    segments.append({key:dataOut})


segmentsJSON = { "segments": segments}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)
