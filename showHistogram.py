#python3 showHistogram.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PlainData.json mobilePhase


import os
import sys
import json
import cv2
import numpy as np
import histogram
import globals
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
key = (sys.argv[2])

#showHistogram(data, title='-', bins=30, show = True, label = None, histtype='bar', stacked = False)

def showFileData(input_file, key):
    global sampleSize
    path, filename = globals.getFileName(input_file)
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    processed = 0
    title = input_file
    segments = segmentsJSON["segments"]
    for segment in segments:
        histogram.showHistogram(segment[key], title, label = [filename])


showFileData(input_file, key)
