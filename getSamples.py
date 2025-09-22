 #python3 getSamples.py ./60hzSegments.json ./60hzSegmentSamples.json

import os
import sys
import json

DISTANCE_FACTOR = 0.3
input_file = (sys.argv[1])
output_file = (sys.argv[2])

with open(input_file, 'r', encoding='utf-8') as f:
    segments = json.load(f)

TMAX_SAMPLE = None

segmentsNew = []
previousTimestamp = None

c = 0
for segment in segments:
    files = segment["files"]
    previousPeriod = float(files[3]["timestamp"]) - float(files[0]["timestamp"])
    TMAX_SAMPLE = DISTANCE_FACTOR*previousPeriod
    previousTimestamp = None
    previousFile = None
    previousSampleTimestamp = None
    segmentNew = {"timestamp": None, "samples": []}
    segmentsNew.append(segmentNew)
    samples = []
    segmentNew["timestamp"] = segment["timestamp"]            #this segment will have the timestamp of its first file
    segmentNew["samples"] = samples
    for file in files:
        timestamp = file["timestamp"]
        if previousTimestamp is None:                   #this is the first file         
            previousTimestamp = timestamp               #previousTimestamp initial value 
            previousFile = file
            
            if previousSampleTimestamp:
                previousPeriod = float(timestamp) - float(previousSampleTimestamp)
                TMAX_SAMPLE = DISTANCE_FACTOR*previousPeriod
            continue            #wait for the next file
            
        if float(timestamp) - float(previousTimestamp) <= TMAX_SAMPLE:        #this is a new sample
            sample = {"timestamp": previousTimestamp, "fileMobileMirror": previousFile, "fileFixedMirror": file}
            samples.append(sample)
            previousSampleTimestamp = previousTimestamp #saved to calculate Period with the next file
            previousFile = None                         #this file has now been used
            previousTimestamp = None
        c+=1
        if c > 4: break
    break

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsNew, f, ensure_ascii=False, indent=4)

