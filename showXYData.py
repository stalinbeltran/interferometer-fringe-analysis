#python3 showXYData.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseSoften.json timestamp fixedPhase:mobilePhase


import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
xkey = (sys.argv[2])
ykey = (sys.argv[3])
ykey = ykey.split(':')

showedSize = None
if len(sys.argv)>4:
    showedSize = int(sys.argv[4])


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

title = input_file
softenedArray = dataJSON
    
for softData in softenedArray:
    begin = 0
    N = 0
    if "N" in softData:
        N = softData["N"]
    size = len(softData["data"][xkey])
    if not showedSize:
        showedSize = size
    for begin in range(0, size, showedSize):
        end = begin + showedSize
        data = softData["data"]
        xdata = data[xkey][begin:end]
        for key in ykey:
            ydata = data[key][begin:end]
            plt.plot(xdata, ydata, '.', label=key + ' vs ' + xkey + " (" + str(begin) + "->" + str(end) + ", N:" + str(N) + ")")
        plt.title(title)
        plt.legend()
        plt.show()
        