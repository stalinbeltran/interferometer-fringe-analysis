#python3 /mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis/procesadorVideos.py /videos 39-40 160
#python /home/stalin/interferometer-fringe-analysis/procesadorVideos.py /home/stalin/interferometer-fringe-analysis /videos 160 39-40

import os
import sys

basePath = sys.argv[1]
input_folder = (sys.argv[2])
fps = int(sys.argv[3])
rangoArchivos = sys.argv[4]
inicio, final = rangoArchivos.split('-')
inicio = int(inicio)
final = int(final)
#basePath = "/mnt/d/Stalin/Desarrollo/interferometer-fringe-analysis"
#basePath = "/home/stalin/interferometer-fringe-analysis"


def run(command, falseFileName, trueFileName):
    command = command.replace(falseFileName, trueFileName)
    os.system(command)


for index in range(inicio, final):
    falseFileName = "fringes_XXX"
    trueFileName = "fringes_" + str(index)
    
    #h264 to mp4
    run("ffmpeg -i " + basePath + "/videos/fringes_XXX.h264 -c copy " + basePath + "/videos/fringes_XXX.mp4", falseFileName, trueFileName)

    #video to frames:
    #create the required folder for the frames    
    run("mkdir " + basePath + "/videos/fringes_XXX", falseFileName, trueFileName)
    run("mv " + basePath + "/videos/fringes_XXX.mp4 " + basePath + "/videos/fringes_XXX/fringes_XXX.mp4", falseFileName, trueFileName)
    run("mkdir " + basePath + "/videos/fringes_XXX/frames", falseFileName, trueFileName)
    #get frames from mp4
    run("ffmpeg -i " + basePath + "/videos/fringes_XXX/fringes_XXX.mp4 -vf fps=" + str(fps) + " " + basePath + "/videos/fringes_XXX/frames/fringes_XXX-%d-.png", falseFileName, trueFileName)

