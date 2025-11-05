#python3 showXYData.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_periscope-PhaseSoften.json timestamp fixedPhase:mobilePhase


import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt
import globals

input_file = (sys.argv[1])
xkey = (sys.argv[2])
ykey = globals.getPromptOptionalParameter(3, [{"func":globals.split, "funcParams":[":"]}])
showedSize = globals.getPromptOptionalParameter(4, [{"func":int}])
Nconstant = globals.getPromptOptionalParameter(5, [{"func":int}])
marker = globals.getPromptOptionalParameter(6)
ylim = globals.getPromptOptionalParameter(7, [{"func":globals.split, "funcParams":[":"]}, {"func":float}])

with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

title = input_file
if not marker:
    marker = '.'
for softData in dataJSON:
    begin = 0
    N = 0
    if "N" in softData:
        N = softData["N"]
    
    data = softData["data"]
    data["SEQUENTIAL"] = range(len(data[ykey[0]]))     #add a new data, a simple sequential value
    if Nconstant and Nconstant != N: continue
    size = len(softData["data"][xkey])
    if not showedSize:
        showedSize = size
    for begin in range(0, size, showedSize):
        end = begin + showedSize
        xdata = data[xkey][begin:end]
        for key in ykey:
            ydata = data[key][begin:end]
            plt.plot(xdata, ydata, marker, label=key + ' vs ' + xkey + " (" + str(begin) + "->" + str(end) + ", N:" + str(N) + ")")
        plt.title(title)
        plt.legend()
        if ylim:
            plt.ylim(ylim[0], ylim[1]) 
        plt.show()
        