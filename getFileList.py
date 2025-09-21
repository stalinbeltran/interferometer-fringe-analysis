#python3 getFileList.py D:\Stalin\FotosFranjasProyecto\60hz ./60hzFiles.json

import os
import sys
import json

input_folder = (sys.argv[1])
output_file = (sys.argv[2])

files = []
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png')):
        parts = filename.split('-')
        timestamp = parts[1]
        absolutePath = os.path.join(input_folder, filename)
        file = {
            "filename": filename,
            "timestamp": timestamp,
            "absolutePath": absolutePath
        }
        files.append(file)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False, indent=4)

