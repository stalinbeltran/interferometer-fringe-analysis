#D:\Stalin\Desarrollo\interferometer-fringe-analysis>python rescaleImage.py ./originales ./recortadas

import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure
import sys
import os

input_folder = (sys.argv[1])
output_folder = (sys.argv[2])
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        inputPath = os.path.join(input_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        outputPath = os.path.join(output_folder, filenameNoExt + "" + file_extension)
        img = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        img2 = exposure.rescale_intensity(img)
        cv2.imwrite(outputPath, img2)



