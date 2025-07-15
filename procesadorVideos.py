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
    falseFileName = "fringes_XXX"
    trueFileName = "fringes_" + str(index)
    
    #h264 to mp4
    run("ffmpeg -i /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.h264 -c copy /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.mp4", falseFileName, trueFileName)

    #video to frames:
    #create the required folder for the frames    
    run("mkdir /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX", falseFileName, trueFileName)
    run("mv /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX.mp4 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/fringes_XXX.mp4", falseFileName, trueFileName)
    run("mkdir /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/frames", falseFileName, trueFileName)
    #get frames from mp4
    run("ffmpeg -i /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/fringes_XXX.mp4 -vf fps=6 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/videos/fringes_XXX/frames/fringes_XXX-%d-.png", falseFileName, trueFileName)

