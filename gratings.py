# gratings.py

import numpy as np
import sys
import matplotlib.pyplot as plt


wavelength = int(sys.argv[1])
angleFraction = int(sys.argv[2])

x = np.arange(-500, 501, 1)
X, Y = np.meshgrid(x, x)

angle = np.pi / angleFraction
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength
)

plt.set_cmap("gray")
plt.subplot(121)
plt.imshow(grating)

# Calculate Fourier transform of grating
ft = np.fft.ifftshift(grating)
ft = np.fft.fft2(ft)
ft = np.fft.fftshift(ft)

plt.subplot(122)
plt.imshow(abs(ft))
plt.xlim([480, 520])
plt.ylim([520, 480])  # Note, order is reversed for y


#plt.show()
print(ft)
rows, cols = np.shape(ft)
print("rows: ", rows, "cols: ", cols)

maxRow = 0
absft = abs(ft)
maxRowValue = 0
for row in range(0, rows):
    max = np.max(absft[row])
    if max > maxRowValue:
        maxRowValue = max
        maxRow = row
    #print(max)
    
print(max)
print(maxRow)