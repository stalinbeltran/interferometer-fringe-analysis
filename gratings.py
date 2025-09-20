# python3 gratings.py 100 0 0

import numpy as np
import sys
import matplotlib.pyplot as plt


wavelength = int(sys.argv[1])
angleFactor = float(sys.argv[2])
phaseFactor = float(sys.argv[3])


x = np.arange(-500, 501, 1)
print('len(x):')
sizex = len(x)
print(sizex)
X, Y = np.meshgrid(x, x)

angle = np.pi * angleFactor
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*phaseFactor
)


plt.set_cmap("gray")
plt.subplot(131)
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*0.2
)
plt.imshow(np.fft.ifftshift(grating))

plt.subplot(132)
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*0.4
)
plt.imshow(np.fft.ifftshift(grating))

plt.subplot(133)
grating = np.sin(
    2*np.pi*(X*np.cos(angle) + Y*np.sin(angle)) / wavelength + np.pi*0.6
)
plt.imshow(np.fft.ifftshift(grating))


plt.show()
exit()



plt.set_cmap("gray")
#plt.subplot(131)
#plt.imshow(grating)

# print("\n\n-------------------\n------------------- grating:")
# print(grating)
# print("\n\n-------------------\n------------------- max(grating):")
# print(np.max(grating))
# print(np.min(grating))

# Calculate Fourier transform of grating
# isft = np.fft.ifftshift(grating)
# sft = np.fft.fftshift(isft)
# plt.subplot(131)
# plt.imshow(isft)
# plt.subplot(133)
# plt.imshow(sft)
plt.show()
exit()

ft = np.fft.ifftshift(grating)
ft = np.fft.fft2(ft)
#ft = np.fft.fftshift(ft)



#ftmod = (abs(ft)*1000).astype(int)
ftmod = abs(ft)
# ftmod /=415411/4
# ftmod -=2
#print("\n\n-------------------\n------------------- ftmod:")

plt.subplot(132)
plt.imshow(ftmod)

diferencia = -490
plt.xlim([0, 500 + diferencia])
plt.ylim([500 + diferencia, 0])  # Note, order is reversed for y


# print("\n\n-------------------\n------------------- max(ftmod):")
# print(np.max(ftmod))
# print(np.min(ftmod))

plt.subplot(133)
angle = np.angle(ft)
angle *= ftmod

#print("\n\n-------------------\n------------------- angle:")
#print(angle)
plt.imshow(angle)

# print("\n\n-------------------\n------------------- max(angle):")
# print(np.max(angle))
# print(np.min(angle))

plt.xlim([0, 500 + diferencia])
plt.ylim([500 + diferencia, 0])  # Note, order is reversed for y

# Calculate frequency components for each dimension
sample_spacing_x = x[1] - x[0]
freq_x = np.fft.fftfreq(sizex, d=sample_spacing_x)

print("\n\n-------------------\n------------------- freq_x:")
print(freq_x)
#print(xxxxxxxxx)


#print(ft)
rows, cols = np.shape(ft)
print("rows: ", rows, "cols: ", cols)

maxRow = 0
absft = abs(ft)
maxRowValue = 0
absftFlat = absft.flatten()
sorted_indices = np.argsort(-absftFlat)

for i in range(0, 2):
    maxPosition = sorted_indices[i]
    print("maxPosition: " + str(maxPosition))
    index = np.unravel_index(maxPosition, np.shape(ft))
    print('index: ', index)
    print(index)
    imaginaryValue = ft[index]
    maxAngle = np.angle(imaginaryValue, True)
    print('maxAngle: ', maxAngle)
    print('freq_x: ', freq_x[index[1]])
    print('periodo: ', 1/freq_x[index[1]])
    


# print(imaginaryValue)
# print(abs(imaginaryValue))
# maxAngle = np.angle(imaginaryValue, True)
# print(maxAngle)

plt.show()
