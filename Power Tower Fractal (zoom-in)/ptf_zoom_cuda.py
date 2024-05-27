import cupy as cp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm
import os

# Initial plot range parameters
px, py = 0, 0  # Starting center
px_target, py_target = -0.43137999995, 0.895038  # Target center for zooming
scale_initial = 5  # Initial scale (half the width/height of the plot range)
zoom_factor = 0.96  # Scale reduction per frame
nx, ny = 1920, 1080
max_iter = 500
escape_radius = 1e+10

def compute_tetration_divergence(nx, ny, max_iter, escape_radius, px, py, scale):
    try:
        x = cp.linspace(px - scale, px + scale, nx)
        y = cp.linspace(py - scale*(9/16), py + scale*(9/16), ny)
        c = x[:, cp.newaxis] + 1j * y[cp.newaxis, :]

        divergence_map = cp.zeros(c.shape, dtype=cp.bool_)
        z = c.copy()

        for k in tqdm(range(max_iter), desc="Calculating Tetration", ncols=100):
            z = cp.power(c, z)
            mask = cp.abs(z) > escape_radius
            divergence_map[mask] = True
            c[mask] = cp.nan  # Escape from further computation for diverged points

        return cp.asnumpy(divergence_map)
    except Exception as e:
        print(f"Error in compute_tetration_divergence: {e}")
        traceback.print_exc()
        return cp.asnumpy(cp.zeros((nx, ny), dtype=cp.bool_))

# Custom colormap: Divergence is white, convergence is black
cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"])

# Set the frame range you want to output
start_frame = 667
end_frame = 800

for frame in range(start_frame-1):
    scale = scale_initial * (zoom_factor ** frame)

    # Gradually move the center towards the target
    px = px + (px_target - px) * (1-zoom_factor)
    py = py + (py_target - py) * (1-zoom_factor)

for frame in range(start_frame, end_frame + 1):
    scale = scale_initial * (zoom_factor ** frame)

    # Gradually move the center towards the target
    px = px + (px_target - px) * (1-zoom_factor)
    py = py + (py_target - py) * (1-zoom_factor)

    # Compute the convergence map
    divergence_map = compute_tetration_divergence(nx, ny, max_iter, escape_radius, px, py, scale)
    
    # Calculate the figure size in inches for 4K resolution
    dpi = 100 # You can adjust this as needed
    fig_width, fig_height = nx / dpi, ny / dpi
    
    # Create figure with the calculated size
    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    
    # Plotting without axes
    plt.imshow(divergence_map.T, extent=[px - scale, px + scale, py - scale * (9 / 16), py + scale * (9 / 16)], origin='lower', cmap=cmap)
    plt.axis('off') # Turn off the axis
    
    # Save the figure without any borders or frames
    plt.savefig(f'tetration_zoom_frame_{frame+1}.png', dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.clf()
