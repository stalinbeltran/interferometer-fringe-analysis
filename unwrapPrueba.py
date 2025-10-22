import numpy as np
import matplotlib.pyplot as plt

# Generate a noisy wrapped phase signal
x = np.linspace(0, 4 * np.pi, 100)
true_phase = np.sin(x) * 5 + x
wrapped_phase = np.arctan2(np.sin(true_phase), np.cos(true_phase)) # Introduces 2pi wraps
noise = np.random.normal(0, 0.7, 100) # Add some noise
noisy_wrapped_phase = wrapped_phase + noise

# Unwrapped phase
unwrapped_phase = np.unwrap(noisy_wrapped_phase)

plt.figure(figsize=(10, 6))
plt.plot(x, true_phase, label='True Phase', linestyle='--')
plt.plot(x, noisy_wrapped_phase, label='Noisy Wrapped Phase')
plt.plot(x, unwrapped_phase, label='Unwrapped Phase')
plt.xlabel('X')
plt.ylabel('Phase')
plt.title('1D Noisy Phase Unwrapping')
plt.legend()
plt.grid(True)
plt.show()