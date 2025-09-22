 #python3 getSamples.py ./60hzSegments.json ./60hzSegmentSamples.json

import os
import sys
import json

DISTANCE_FACTOR = 0.5
input_file = (sys.argv[1])
output_file = (sys.argv[2])

with open(input_file, 'r', encoding='utf-8') as f:
    segmentsJSON = json.load(f)

segments = segmentsJSON["segments"]
TMAX_SAMPLE = None

segmentsNew = []
previousTimestamp = None

fileCounter = 0
sampleCounter = 0
for segment in segments:
    files = segment["files"]
    if len(files) < 3:
        #print("Files not used:")
        #print(files)
        continue                 #we need al least 3 files
    previousPeriod = float(files[2]["timestamp"]) - float(files[0]["timestamp"])
    TMAX_SAMPLE = DISTANCE_FACTOR*previousPeriod
    
    #print("previousPeriod:", previousPeriod)
    #print("TMAX_SAMPLE:", TMAX_SAMPLE)
    previousTimestamp = None
    previousFile = None
    previousSampleTimestamp = None
    segmentNew = {"timestamp": None, "samples": []}
    segmentsNew.append(segmentNew)
    samples = []
    segmentNew["timestamp"] = segment["timestamp"]            #this segment will have the timestamp of its first file
    segmentNew["samples"] = samples
    for file in files:
        fileCounter+=1
        timestamp = file["timestamp"]
        #print("timestamp:", timestamp)
        if previousTimestamp is None:                   #this is the first file         
            previousTimestamp = timestamp               #previousTimestamp initial value 
            previousFile = file
            
            if previousSampleTimestamp:
                previousPeriod = float(timestamp) - float(previousSampleTimestamp)
                TMAX_SAMPLE = DISTANCE_FACTOR*previousPeriod
            continue            #wait for the next file
        dif = float(timestamp) - float(previousTimestamp)
        #print("dif:", dif)
        
        #print("previousPeriod:", previousPeriod)
        #print("TMAX_SAMPLE:", TMAX_SAMPLE)
        if dif <= TMAX_SAMPLE:        #this is a new sample
            sampleCounter+=1
            sample = {"timestamp": previousTimestamp, "fileMobileMirror": previousFile, "fileFixedMirror": file}
            samples.append(sample)
            previousSampleTimestamp = previousTimestamp #saved to calculate Period with the next file
            previousFile = None                         #this file has now been used
            previousTimestamp = None
        #if fileCounter > 10: break
    if fileCounter > 2*sampleCounter + 2:
        print("fileCounter: ", fileCounter)
        print("sampleCounter: ", sampleCounter)
        print("file:", file)
        break


segmentsJSON = {"segments": segmentsNew}
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

