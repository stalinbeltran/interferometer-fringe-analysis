import numpy as np
import matplotlib.pyplot as plt

# 1. Create a sample signal
# x = np.arange(0, 2*np.pi, 0.1)
x = np.linspace(0, 2 * np.pi, 100)
signal = np.sin(3*x) + 0.5 * np.cos(2 * x)

# 2. Compute the Fourier Transform
fourier_transform = np.fft.fft(signal)

# 3. Manipulate the frequency data (e.g., apply a low-pass filter)
# Keep only the first few frequency components
cutoff = 5
fourier_transform[cutoff:-cutoff] = 0

# 4. Perform the Inverse Fourier Transform
reconstructed_signal = np.fft.ifft(fourier_transform)

# 5. Visualize the results
plt.figure(figsize=(10, 6))
plt.plot(x, signal, label='Original Signal')
plt.plot(x, reconstructed_signal, label='Reconstructed Signal')
plt.legend()
plt.title('Fourier Reconstruction')
plt.show()
