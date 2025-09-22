 #python3 getSegments.py ./60hzFiles.json ./60hzSegments.json

import os
import sys
import json

RMPMAX = 400
input_file = (sys.argv[1])
output_file = (sys.argv[2])

with open(input_file, 'r', encoding='utf-8') as f:
    files = json.load(f)

TMAX = 2*(1/(RMPMAX/60))

segments = []           #list of segments
previousTimestamp = None
segment = {"files": [], "timestamp": files[0]["timestamp"]}
segments.append(segment)
for file in files:
    timestamp = file["timestamp"]
    if previousTimestamp is None:                   #this is the first file         
        previousTimestamp = timestamp               #previousTimestamp initial value 
    if float(timestamp) - float(previousTimestamp) > TMAX:        #this is a new segment
        segment = {"files": [], "timestamp": None}
        segment["timestamp"] = timestamp            #this segment will have the timestamp of its first file
        segments.append(segment)                    #add the new segment

    previousTimestamp = timestamp
    segment["files"].append(file)                   #always add this file to actual segment (it should belong to one segment at least)

segmentsJSON = {"segments": segments}
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segmentsJSON, f, ensure_ascii=False, indent=4)

