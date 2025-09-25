#python3 getPeriodPhase.py D:\Stalin\FotosFranjasProyecto\viernesXXX\results\40hzSegmentSamplesFFT.json D:\Stalin\FotosFranjasProyecto\viernesXXX\results\40hzSegmentSamplesPeriodPhase.json


import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getPeriods(ftOrdered):
    periods = []
    for ftItem in ftOrdered:
        frequency = ftItem["frequency"]
        if frequency == 0: continue         #discard constant signal
        period = 1/frequency
        ft = complex(ftItem["ft"]["real"], ftItem["ft"]["imag"])
        phase = np.angle(ft, True)
        periods.append({"period": period, "phase":phase })
    return periods



with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
for segment in segments:
    samples = segment["samples"]
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        if "periods" not in fileMobile:
            fileMobile["periods"] = getPeriods(fileMobile["fftParams"])
            processed+=1

        if "periods" not in fileFixed:
            fileFixed["periods"] = getPeriods(fileFixed["fftParams"])
            processed+=1
        if processed > 10: break
print("processed: ", processed)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)
