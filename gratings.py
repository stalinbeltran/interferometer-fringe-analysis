# gratings.py

import numpy as np
import sys
import matplotlib.pyplot as plt


wavelength = int(sys.argv[1])
x = np.arange(-500, 501, 1)

y = np.sin(2 * np.pi * x / wavelength)

plt.plot(x, y)
plt.show()