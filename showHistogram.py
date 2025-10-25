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
keys = (sys.argv[2])
keys = keys.split(":")
histogramRange = None
if len(sys.argv)>3:
    histogramRangeS = (sys.argv[3])
    histogramRangeS = histogramRangeS.split(':')
    histogramRange = (float(histogramRangeS[0]), float(histogramRangeS[1]))

#showHistogram(data, title='-', bins=30, show = True, label = None, histtype='bar', stacked = False)

def showFileData(input_file, keys, histogramRange):
    global sampleSize
    path, filename = globals.getFileName(input_file)
    with open(input_file, 'r', encoding='utf-8') as f:
        dataJSON = json.load(f)

    title = input_file
    for data in dataJSON:
        labels = []
        datas = []
        for key in keys:
            label = key + " N = " + str(data["N"])
            labels.append(label)
            datas.append(data["data"][key])
        if histogramRange:
            histogram.showHistogram(datas, title, label = labels, histogramRange = histogramRange)
        else:
            histogram.showHistogram(datas, title, label = labels)


showFileData(input_file, keys, histogramRange)
