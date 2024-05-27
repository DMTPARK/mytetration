import numpy as np
import matplotlib.pyplot as plt

# Function to perform the tetration operation and check for convergence using vectorization
def compute_tetration_convergence(base, nx, ny, max_iter, threshold, escape_radius):
    # Expanding the range for real and imaginary parts
    x = np.linspace(4, 6, nx)
    y = np.linspace(-1, 1, ny)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]

    # Initialize z with c
    z = c.copy()
    prev_z = z.copy()

    convergence_map = np.zeros_like(c, dtype=bool)

    for k in range(max_iter):
        z = base ** z
        escaped = np.abs(z) > escape_radius
        converged = np.abs(z - prev_z) < threshold
        convergence_map = np.logical_or(convergence_map, converged)
        
        # Stop updating z for points that have already converged or escaped
        z = np.where(converged | escaped, prev_z, z)
        prev_z = z.copy()
        
        # If all points have converged or escaped, stop early
        if np.all(converged | escaped):
            break

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