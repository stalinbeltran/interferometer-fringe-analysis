 #python3 getSegments.py ./60hzFiles.json

import os
import sys
import json

RMPMAX = 400
input_file = (sys.argv[1])
output_file = (sys.argv[2])

with open(input_file, 'r', encoding='utf-8') as f:
    files = json.load(files, f)

TMAX = 2*(1/(RMPMAX/60))

segments = []           #list of segments
segment = {
    "files": [],        #array of all its files
    "timestamp" None    #the timestamp of its first file, as a reference
    }
segments.append(segment)    #add the first segment
previousTimestamp = None
for file in files:
    timestamp = file["timestamp"]
    if previousTimestamp is None:                   #this is the first file
        segment["files"].append(file)                #always add this file to actual segment (it should belong to one segment at least)
        segment["timestamp"] = timestamp            #this segment will have the timestamp of its first file
        previousTimestamp = timestamp
        continue
    if timestamp - previousTimestamp > TMAX:        #this is a new segment
        segment = {"files": [], "timestamp" None}
        segment["files"].append(file)                #always add this file to actual segment (it should belong to one segment at least)
        segment["timestamp"] = timestamp
        segments.append(segment)                    #add the new segment

    previousTimestamp = timestamp
    segment["files"].append(file)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(segments, f, ensure_ascii=False, indent=4)

