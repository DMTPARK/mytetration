import numpy as np
import matplotlib.pyplot as plt
from numba import jit, prange

# JIT-compiled function to perform the tetration operation and check for convergence
@jit(nopython=True, parallel=True)
def compute_tetration_convergence(base, nx, ny, max_iter, threshold, escape_radius):
    x = np.linspace(4, 6, nx)
    y = np.linspace(-1, 1, ny)
    convergence_map = np.zeros((nx, ny), dtype=np.bool_)

    for i in prange(nx):
        for j in range(ny):
            z = x[i] + 1j * y[j]
            prev_z = z
            for k in range(max_iter):
                z = base ** z
                if np.abs(z) > escape_radius:
                    break
                if np.abs(z - prev_z) < threshold:
                    convergence_map[i, j] = True
                    break
                prev_z = z

    return convergence_map

# Parameters
nx, ny = 500, 500
max_iter = 50
threshold = 1e-5
escape_radius = 1e10
base = np.sqrt(2)

# Compute the convergence map using JIT compilation
convergence_map = compute_tetration_convergence(base, nx, ny, max_iter, threshold, escape_radius)

# Plotting
plt.imshow(convergence_map.T, extent=[4, 6, -1, 1], origin='lower')
plt.xlabel('Real part')
plt.ylabel('Imaginary part')
plt.title('Convergence and Divergence in Tetration with √2')
plt.colorbar(label='Convergence (1) / Divergence (0)')
plt.show()