# gratings.py

import numpy as np
import sys
import matplotlib.pyplot as plt


wavelength = int(sys.argv[1])
angleFactor = float(sys.argv[2])
phaseFactor = float(sys.argv[3])

x = np.arange(-500, 501, 1)
X, Y = np.meshgrid(x, x)

angle = np.pi * angleFactor
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*phaseFactor
)

plt.set_cmap("gray")
plt.subplot(131)
plt.imshow(grating)
# print("\n\n-------------------\n------------------- grating:")
# print(grating)
# print("\n\n-------------------\n------------------- max(grating):")
# print(np.max(grating))
# print(np.min(grating))

# Calculate Fourier transform of grating
ft = np.fft.ifftshift(grating)
ft = np.fft.fft2(ft)
ft = np.fft.fftshift(ft)

plt.subplot(132)
#ftmod = (abs(ft)*1000).astype(int)
ftmod = abs(ft)
ftmod /=415411/4
ftmod -=2
#print("\n\n-------------------\n------------------- ftmod:")
ftmod[0:100, :] = grating[0:100, :]
plt.imshow(ftmod)
#print(ftmod)
diferencia = 20
plt.xlim([500 - diferencia, 500 + diferencia])
plt.ylim([500 + diferencia, 500-diferencia])  # Note, order is reversed for y


# print("\n\n-------------------\n------------------- max(ftmod):")
# print(np.max(ftmod))
# print(np.min(ftmod))

plt.subplot(133)
angle = np.angle(ft)

#print("\n\n-------------------\n------------------- angle:")
#print(angle)
plt.imshow(angle)

print("\n\n-------------------\n------------------- max(angle):")
print(np.max(angle))
print(np.min(angle))

plt.xlim([500 - diferencia, 500 + diferencia])
plt.ylim([500 + diferencia, 500-diferencia])  # Note, order is reversed for y


#print(ft)
rows, cols = np.shape(ft)
print("rows: ", rows, "cols: ", cols)

maxRow = 0
absft = abs(ft)
maxRowValue = 0
maxPosition = np.argmax(absft)
print("maxPosition:" + str(maxPosition))
index = np.unravel_index(maxPosition, np.shape(ft))
imaginaryValue = ft[index]
print(imaginaryValue)
print(abs(imaginaryValue))
maxAngle = np.angle(imaginaryValue, True)
print(maxAngle)

#plt.show()
