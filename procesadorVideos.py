#python3 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/procesadorVideos.py /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos 39-40

import os
import sys

input_folder = (sys.argv[1])
rangoArchivos = sys.argv[2]
inicio, final = rangoArchivos.split('-')
inicio = int(inicio)
final = int(final)

def run(command, falseFileName, trueFileName):
    command = command.replace(falseFileName, trueFileName)
    os.system(command)


for index in range(inicio, final):
    #h264 to mp4
    command = "ffmpeg -i /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.h264 -c copy /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.mp4"
    run(command, "fringes_XXX", "fringes_" + str(index))
    sys.exit(9)

    #video to frames:
    #create the required folder for the frames
    command = "mkdir /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/frames"
    command = command.replace("fringes_XXX", "fringes_" + str(index))
    os.system(command)
    #get frames from mp4
    command = "ffmpeg -i /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/fringes_XXX.mp4 -vf fps=6 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/frames/fringes_XXX-%d-.png"
    command = command.replace("fringes_XXX", "fringes_" + str(index))
    os.system(command)

