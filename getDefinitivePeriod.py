#python3 getDefinitivePeriod.py D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesFirstPeriod.json D:\Stalin\FotosFranjasProyecto\friday19092025\results\40hzSegmentSamplesDefinitivePeriod.json 128


import os
import sys
import json
import cv2
import numpy as np

input_file = (sys.argv[1])
output_file = (sys.argv[2])

def getDefinitivePeriod(periods, lookedPeriod):
    all_periods = [d for d in periods if abs(d['period'] - lookedPeriod) < 1]
    try:
        return all_periods[0]
    except:
        return None



with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
processed = 0
nulls = 0
for segment in segments:
    lookedPeriod = segment["lookedPeriod"]
    samples = segment["samples"]
    for sample in samples:
        fileMobile = sample["fileMobileMirror"]
        fileFixed = sample["fileFixedMirror"]
        if "period" not in fileMobile or "period" not in fileFixed:
            print("period not in fileMobile or fileFixed. Timestamp: ", sample["timestamp"])
            if "periods" in fileMobile:
                del fileMobile["periods"]
            if "periods" in fileFixed:
                del fileFixed["periods"]
            continue
        if abs(fileMobile["period"]["period"] - lookedPeriod) > 1 :
            fileMobile["period"] = getDefinitivePeriod(fileMobile["periods"], lookedPeriod)
            processed+=1

        if abs(fileFixed["period"]["period"] - lookedPeriod) > 1 :
            fileFixed["period"] = getDefinitivePeriod(fileFixed["periods"], lookedPeriod)
            processed+=1
        if fileMobile["period"] is None:
            nulls+=1
            if nulls < 10:
                print("lookedPeriod: ", lookedPeriod)
                print(fileMobile["periods"])
        if fileFixed["period"] is None:
            nulls+=1
            if nulls < 10:
                print("lookedPeriod: ", lookedPeriod)
                print(fileFixed["periods"])
        del fileMobile["periods"]
        del fileFixed["periods"]
    # if processed > 0: break
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

print("processed (period fixed samples): ", processed)
print("nulls: ", nulls)