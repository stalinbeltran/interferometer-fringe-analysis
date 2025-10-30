#python3 

import os
import sys
import json
import cv2
import numpy as np
import globals
from collections import deque

input_file = (sys.argv[1])
output_file = (sys.argv[2])
displacement = globals.getPromptOptionalParameter(3, [{"func":float}])    #6.87




with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
hz = data[0]["data"]["hz"]
hzReference = [-1*(x - displacement)/6 for x in hz]
data[0]["data"]["hzReference"] = hzReference

print("end")


with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("ended")
