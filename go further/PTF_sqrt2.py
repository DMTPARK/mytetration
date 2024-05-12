import numpy as np
import matplotlib.pyplot as plt

# Function to check if a sequence converges
def is_convergent(seq, threshold):
    # Check if the absolute difference between last two elements is below the threshold
    return np.abs(seq[-1] - seq[-2]) < threshold

# Function to perform the tetration operation and check for convergence
def compute_tetration_convergence(base, nx, ny, max_iter, threshold, escape_radius):
    # Expanding the range for real and imaginary parts
    x = np.linspace(4, 6, nx)
    y = np.linspace(-1, 1, ny)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]

    convergence_map = np.zeros_like(c, dtype=bool)

    for i in range(nx):
        for j in range(ny):
            z = c[i, j]
            seq = [z]

            for k in range(max_iter):
                z = base ** z
                seq.append(z)
                if np.abs(z) > escape_radius or is_convergent(seq, threshold):
                    break

            convergence_map[i, j] = is_convergent(seq, threshold)

    return convergence_map

# Parameters
nx, ny = 500, 500
max_iter = 50
threshold = 1e-5
escape_radius = 1e10
base = np.sqrt(2)

# Compute the convergence map
convergence_map = compute_tetration_convergence(base, nx, ny, max_iter, threshold, escape_radius)

# Plotting
plt.imshow(convergence_map.T, extent=[4, 6, -1, 1], origin='lower')
plt.xlabel('Real part')
plt.ylabel('Imaginary part')
plt.title('Convergence and Divergence in Tetration with √2')
plt.colorbar(label='Convergence (1) / Divergence (0)')
plt.show()
