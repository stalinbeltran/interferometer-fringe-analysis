import numpy as np
import matplotlib.pyplot as plt


def filter(signal, cutoff = 25):
    fourier_transform = np.fft.fft(signal)
    fourier_transform[cutoff:-cutoff] = 0       #low pass filter
    reconstructed_signal = np.fft.ifft(fourier_transform) #Inverse Fourier Transform
    return reconstructed_signal


# 1. Create a sample signal
# x = np.arange(0, 2*np.pi, 0.1)
x = np.linspace(0, 2 * np.pi, 100)
signal = np.sin(6*x) + 0.5 * np.cos(2 * x) + np.sin(60*x)

reconstructed_signal = filter(signal)

# 5. Visualize the results
plt.figure(figsize=(10, 6))
plt.plot(x, signal, label='Original Signal')
plt.plot(x, reconstructed_signal, label='Reconstructed Signal')
plt.legend()
plt.title('Fourier Reconstruction')
plt.show()
