#python imageVerticalCentralCropper.py 800  ./originales ./recortadas

import os
import sys

input_folder = (sys.argv[1])
rangoArchivos = sys.argv[2]
inicio, final = rangoArchivos.split('-')
inicio = int(inicio)
final = int(final)

for index in range(inicio, final):
    command = "ffmpeg -i /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.h264 -c copy /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.mp4"
    command = command.replace("fringes_XXX", "fringes_" + str(index))
    os.system(command)
