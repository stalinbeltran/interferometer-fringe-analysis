

import os
import sys
import json
import cv2
import numpy as np
import globals

input_file = (sys.argv[1])
output_file = (sys.argv[2])


with open(input_file, 'r', encoding='utf-8') as f:
    dataJSON = json.load(f)


with open(output_file, 'r', encoding='utf-8') as f:
    dataJSONoutput = json.load(f)
    
dataJSONoutput.append(dataJSON)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dataJSONoutput, f, ensure_ascii=False, indent=4)


