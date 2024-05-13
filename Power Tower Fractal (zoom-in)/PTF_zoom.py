import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Initial plot range parameters
px, py = 0, 0  # Starting center
px_target, py_target = -0.43137999995, 0.895038  # Target center for zooming
scale_initial = 5  # Initial scale (half the width/height of the plot range)
zoom_factor = 0.96  # Scale reduction per frame
#n_frames = 680 > 10^-12 order 까지 줌
nx, ny = 3840, 2160
max_iter = 500
escape_radius = 1e+10

def compute_tetration_divergence(nx, ny, max_iter, escape_radius, px, py, scale):
    x = np.linspace(px - scale, px + scale, nx)
    y = np.linspace(py - scale*(9/16), py + scale*(9/16), ny)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]

    divergence_map = np.zeros_like(c, dtype=bool)

    for i in range(nx):
        for j in range(ny):
            c_val = c[i, j]
            z = c_val

            for k in range(max_iter):
                z = c_val ** z
                if np.abs(z) > escape_radius:
                    divergence_map[i, j] = True
                    break

    return divergence_map

# 커스텀 컬러맵 생성: 발산은 흰색, 수렴은 검은색
cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"])

# Set the frame range you want to output
start_frame = 667  # Starting at the start_frame+1th frame
end_frame = 800   # Ending at the end_frame+1th frame

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
    dinvergence_map = compute_tetration_divergence(nx, ny, max_iter, escape_radius, px, py, scale)
    
    # Calculate the figure size in inches for 4K resolution
    dpi = 100 # You can adjust this as needed
    fig_width, fig_height = nx / dpi, ny / dpi
    
    # Create figure with the calculated size
    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    
    # Plotting without axes
    plt.imshow(dinvergence_map.T, extent=[px - scale, px + scale, py - scale * (9 / 16), py + scale * (9 / 16)], origin='lower', cmap=cmap)
    plt.axis('off') # Turn off the axis
    
    # Save the figure without any borders or frames
    plt.savefig(f'tetration_zoom_frame_{frame+1}.png', dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.clf()
