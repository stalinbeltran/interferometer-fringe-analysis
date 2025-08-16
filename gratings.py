# gratings.py

import numpy as np
import sys
import matplotlib.pyplot as plt


wavelength = int(sys.argv[1])
angleFraction = int(sys.argv[2])
phaseFactor = float(sys.argv[3])

x = np.arange(-500, 501, 1)
X, Y = np.meshgrid(x, x)

angle = np.pi / angleFraction
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*phaseFactor
)

plt.set_cmap("gray")
plt.subplot(131)
plt.imshow(grating)

# Calculate Fourier transform of grating
ft = np.fft.ifftshift(grating)
ft = np.fft.fft2(ft)
ft = np.fft.fftshift(ft)

plt.subplot(132)
plt.imshow(abs(ft))
plt.subplot(133)
plt.imshow(np.angle(ft))
plt.xlim([480, 520])
plt.ylim([520, 480])  # Note, order is reversed for y


#print(ft)
rows, cols = np.shape(ft)
print("rows: ", rows, "cols: ", cols)

maxRow = 0
absft = abs(ft)
maxRowValue = 0
maxPosition = np.argmax(absft)
print(maxPosition)
index = np.unravel_index(maxPosition, np.shape(ft))
imaginaryValue = ft[index]
print(imaginaryValue)
print(abs(imaginaryValue))
maxAngle = np.angle(imaginaryValue, True)
print(maxAngle)

plt.show()
