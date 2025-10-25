#python3 getSamples.py ./60hzSegments.json ./60hzSegmentSamples.json
#python3 getSamples.py ./40hzSegments.json ./40hzSegmentSamples.json

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
processed = 0
noTimestampCounter = 0
timestamps = []
deltatime = []
c = 0
for segment in segments:
    files = segment["files"]
    if len(files) < 3:
        print("Files not used:")
        print(files)
        continue                 #we need al least 3 files
    previousPeriod = float(files[2]["timestamp"]) - float(files[0]["timestamp"])    #get a tentative initial period for a sample
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
        c +=1
        timestamp = file["timestamp"]
        timestamps.append(float(timestamp))
        if previousTimestamp is None:                   #this is the first file         
            previousTimestamp = timestamp               #previousTimestamp initial value 
            previousFile = file
            
            if previousSampleTimestamp:
                previousPeriod = float(timestamp) - float(previousSampleTimestamp)
                TMAX_SAMPLE = DISTANCE_FACTOR*previousPeriod
            continue            #wait for the next file
            
        timestampDiff =  float(timestamp) - float(previousTimestamp)
        deltatime.append(timestampDiff)
        if timestampDiff <= TMAX_SAMPLE:        #this is a new sample
            sample = {"timestamp": previousTimestamp, "fileMobileMirror": previousFile, "fileFixedMirror": file}
            samples.append(sample)
            previousSampleTimestamp = previousTimestamp #saved to calculate Period with the next file
            previousFile = None                         #this file has now been used
            previousTimestamp = None
            processed+=1
        else:
            noTimestampCounter+=1
            if noTimestampCounter < 10:
                print("TMAX_SAMPLE: ", TMAX_SAMPLE)
                print("timestampDiff: ", timestampDiff)
            previousTimestamp = timestamp               #this is now the previous timestamp
            previousFile = file                         #this is the previous file

print("processed: ", processed)
segmentsJSON = {"segments": segmentsNew}
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

newData = [
        {
            "N" : 0,
            "data" : {
                "timestamp" : timestamps,
                "deltatime" : deltatime
            }
        }
    ]
    
with open("D:\\Stalin\\FotosFranjasProyecto\\results\\timestamps.json", 'w', encoding='utf-8') as f:
    json.dump(newData, f, ensure_ascii=False, indent=4)

