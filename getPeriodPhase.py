#python3 getPeriodPhase.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesFFT.json D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesPeriodPhase.json


import os
import sys
import json
import cv2
import numpy as np
import phaseProcessing
 
input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getPeriods(ftOrdered):
    periods = []
    for ftItem in ftOrdered:
        frequency = ftItem["frequency"]
        period = 1/frequency
        ft = complex(ftItem["ft"]["real"], ftItem["ft"]["imag"])
        phase = np.angle(ft, True)
        phase = phaseProcessing.getPositivePhaseDegrees(phase)
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
        if fileMobile["fftParams"] is None or fileFixed["fftParams"] is None:
            del fileFixed["fftParams"]
            del fileMobile["fftParams"]
            continue      #ignore this sample, as there are not fftParams
        if "periods" not in fileMobile:
            fileMobile["periods"] = getPeriods(fileMobile["fftParams"])
            processed+=1

        if "periods" not in fileFixed:
            fileFixed["periods"] = getPeriods(fileFixed["fftParams"])
            processed+=1
        del fileFixed["fftParams"]
        del fileMobile["fftParams"]
        #if processed > 10: break
        
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

print("processed: ", processed)