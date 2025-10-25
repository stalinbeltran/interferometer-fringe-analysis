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
previousTimestamp = None
timestamps = []
deltatime = []

for segment in segments:
    files = segment["files"]
    for file in files:
        timestamp = file["timestamp"]
        timestamps.append(float(timestamp))
        timestampDiff =  float(timestamp) - float(previousTimestamp)
        deltatime.append(timestampDiff)


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

