#python3 showPhaseShift.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesPhaseShift.json  

import os
import sys
import json
import cv2
import numpy as np
import histogram
import phaseProcessing
import matplotlib.pyplot as plt

input_file = (sys.argv[1])
sampleSize = int(sys.argv[2])



def showFileData(input_file):
    global sampleSize
    with open(input_file, 'r', encoding='utf-8') as f:
        segmentsJSON = json.load(f)

    processed = 0
    title = input_file
    segments = segmentsJSON["segments"]
    for segment in segments:
        plt.plot(segment["timestamp"], segment["fixedPhase"], '-', label='Fixed')
        plt.plot(segment["timestamp"], segment["mobilePhase"], '-', label='Fixed')
        # plt.plot(segmentTimestamps, segmentMobilePhase, '-', label='Mobile')
        # plt.plot(segmentTimestamps, segmentHzModified, '.', label='Speed (Hz)')
        plt.title(title)
        plt.legend()
        plt.show()


showFileData(input_file)