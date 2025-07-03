#python imageVerticalCentralCropper.py 800  ./originales ./recortadas
from PIL import Image
import os
import sys
import imageSineFit as isf

rangoArchivos = sys.argv[1]
inicio, final = rangoArchivos.split('-')
input_folder = (sys.argv[2])

os.makedirs(output_folder, exist_ok=True)

for index in rangoArchivosArray:
    command = "ffmpeg -i /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.h264 -c copy /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.mp4"
    command.replace("fringes_XXX", "fringes_" + index)
    os.system(command)
