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
plt.imshow(grating)
plt.show()