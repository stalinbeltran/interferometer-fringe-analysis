#python3 blurImages.py ./videos/fringes_65/frames ./videos/fringes_65/framesSoftened

import numpy as np
import cv2
import os
import file
import sys
import imageSineFit as isf
import blurImage as blur

input_folder = (sys.argv[1])
output_folder = (sys.argv[2])
file.createDirectory(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png')):
        inputPath = os.path.join(input_folder, filename)
        filenameNoExt, file_extension = os.path.splitext(filename)
        img1 = cv2.imread(inputPath, cv2.IMREAD_GRAYSCALE)
        outputPath = os.path.join(output_folder, filenameNoExt + "" + file_extension)
        cv2.imwrite(outputPath, imgBlurred)
        break
cv2.destroyAllWindows()












archivoProcesar = (sys.argv[1])

wavelength = 0
angleFactor = 0
phaseFactor = 0

x = np.arange(-500, 501, 1)

X, Y = np.meshgrid(x, x)

angle = np.pi * angleFactor
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*phaseFactor
)

plt.set_cmap("gray")
plt.subplot(131)
grating = cv2.imread(archivoProcesar, 0)
plt.imshow(np.fft.ifftshift(grating))

print("grating.shape")
print()
sizex = grating.shape[1]        #number of columns
print(sizex)





plt.set_cmap("gray")
plt.subplot(131)
plt.imshow(grating)

ft = np.fft.ifftshift(grating)
ft = np.fft.fft2(ft)

ftmod = abs(ft)
plt.subplot(132)
plt.imshow(ftmod)

plt.subplot(133)
angle = np.angle(ft)
angle *= ftmod

# Calculate frequency components for each dimension
sample_spacing_x = 1
freq_x = np.fft.fftfreq(sizex, d=sample_spacing_x)

rows, cols = np.shape(ft)
print("rows: ", rows, "cols: ", cols)

maxRow = 0
absft = abs(ft)
maxRowValue = 0
absftFlat = absft.flatten()
sorted_indices = np.argsort(-absftFlat)

for i in range(0, 10):
    maxPosition = sorted_indices[i]
    print("maxPosition: " + str(maxPosition))
    index = np.unravel_index(maxPosition, np.shape(ft))
    print('index: ', index)
    print(index)
    imaginaryValue = ft[index]
    maxAngle = np.angle(imaginaryValue, True)
    
    print('magnitude: ', absftFlat[i]/1000000)
    print('maxAngle: ', maxAngle)
    print('freq_x: ', freq_x[index[1]])
    print('periodo: ', 1/freq_x[index[1]])
    print("\n")
    

