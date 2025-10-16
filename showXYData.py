#python3 showXYData.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-PlainData.json timestamp mobilePhase


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

#sampleSize = int(sys.argv[4])



def showFileData(input_file):
    global sampleSize
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    processed = 0
    title = input_file
    segments = segmentsJSON["segments"]
    for segment in segments:
        plt.plot(segment[xkey], segment[ykey], '.', label='ykey')
        plt.title(title)
        plt.legend()
        plt.show()


showFileData(input_file)