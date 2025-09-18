
import numpy as np
import matplotlib.pyplot as plt

# Create a sample 2D signal (e.g., a simple sine wave pattern)
N_rows, N_cols = 100, 100
x = np.linspace(0, 10, N_cols, endpoint=False)
y = np.linspace(0, 10, N_rows, endpoint=False)
print('x:')
print(x)
X, Y = np.meshgrid(x, y)
signal = np.sin(2 * np.pi * (0.5 * X + 0.2 * Y))

# Perform 2D FFT
fft_output = np.fft.fft2(signal)

# Shift the zero-frequency component to the center
shifted_fft_output = np.fft.fftshift(fft_output)

# Calculate frequency components for each dimension
sample_spacing_x = x[1] - x[0]
sample_spacing_y = y[1] - y[0]
freq_x = np.fft.fftfreq(N_cols, d=sample_spacing_x)
freq_y = np.fft.fftfreq(N_rows, d=sample_spacing_y)

print('freq_x:')
print(freq_x)

# Shift the frequency arrays to match the shifted FFT output
shifted_freq_x = np.fft.fftshift(freq_x)
shifted_freq_y = np.fft.fftshift(freq_y)

print('shifted_freq_x:')
print(shifted_freq_x)

# Visualize the magnitude spectrum
plt.imshow(np.log(np.abs(shifted_fft_output)), cmap='gray',
           extent=[shifted_freq_x.min(), shifted_freq_x.max(),
                   shifted_freq_y.min(), shifted_freq_y.max()])
plt.xlabel("Frequency (x-direction)")
plt.ylabel("Frequency (y-direction)")
plt.title("2D FFT Magnitude Spectrum")
plt.colorbar(label="Log Magnitude")
#plt.show()

