#python3 showXYData.py D:\Stalin\FotosFranjasProyecto\results\thursday09102025_slowacceleration_direct-DeltaPhase.json hz deltaPhase


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


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)

title = input_file
softenedArray = dataJSON["softened"]
noises = []
for softData in softenedArray:
    plt.plot(softData["data"][xkey], softData["data"][ykey], '.', label='ykey')
    plt.title(title)
    plt.legend()
    plt.show()
    