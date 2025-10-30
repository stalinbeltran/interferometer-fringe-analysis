
import os
import sys
import json

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
    previousTimestamp = files[0]["timestamp"]
    for file in files:
        timestamp = file["timestamp"]
        timestamps.append(float(timestamp))
        timestampDiff =  float(timestamp) - float(previousTimestamp)
        deltatime.append(timestampDiff)
        previousTimestamp = timestamp


newData = [
        {
            "N" : 0,
            "data" : {
                "timestamp" : timestamps,
                "deltatime" : deltatime
            }
        }
    ]
    
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(newData, f, ensure_ascii=False, indent=4)

