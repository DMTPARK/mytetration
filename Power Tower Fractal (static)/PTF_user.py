import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from concurrent.futures import ThreadPoolExecutor

#parameters - plot영역설정관련
x0i = input("Please Enter the x. #(x0) :Plot area center coordinates (default: 0)\n")
try:
    x0 = float(x0i)
except ValueError:
    x0 = 0

y0i = input("Please Enter the y. #(y0) : Plot area center coordinates (default: 0)\n") #(x0,y0) : plot영역 중심좌표
try:
    y0 = float(y0i)
except ValueError:
    y0 = 0

epsi = input("Please Enter the eps. # Plot with an epsilon margin on the left and right of x0 (default: 5e0)\n") #x0 좌우로 eps만큼 plot함
try:
    eps = float(epsi)
except ValueError:
    eps = 5e0

ni = input("Please Enter the n. # Parameter for adjusting the number of pixels\n(3840: approximately 4K resolution, 1920: Full HD resolution) (default: 500)\n") #화소수조절을 위한 parameter (3840:대략 4K화질, 1920:Full HD 화질)
try:
    n = int(ni)
except ValueError:
    n = 500

roti = input("Rotate? (y/N)\n")
try:
    rot = roti
except ValueError:
    rot = "N"

ratioi = input("Ratio(n/n) (default: 1/1)")
try:
    ratio = float(ratioi)
except ValueError:
    ratio = float(1/1)

eps_y = eps * ratio
nx, ny = n, int(n*ratio)

#parameters - tetration계산 관련
max_iter = 500 #최대 몇층까지 계산할 것인지를 정함. max_iter층 만큼 계산했는데 복소수 크기가 escape_radius를 벗어나지 않으면 수렴한것으로 처리.
escape_radius = 1e+10 #복소수크기가 escape_radius를 벗어나면 발산한 것으로 처리함.

#tetration 계산을 위한 함수설정
def compute_point(i, j, c, max_iter, escape_radius):
    c_val = c[i, j]
    z = c_val
    for k in range(max_iter):
        z = c_val ** z
        if np.abs(z) > escape_radius:
            print(f"{i},{j}")
            return i, j, True
    return i, j, False

def compute_tetration_divergence(n, max_iter, escape_radius):
    x = np.linspace(x0 - eps, x0 + eps, n)
    y = np.linspace(y0 - eps, y0 + eps, n)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]

    divergence_map = np.zeros((n, n), dtype=bool)
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(n):
            for j in range(n):
                futures.append(executor.submit(compute_point, i, j, c, max_iter, escape_radius))
        
        for future in futures:
            i, j, diverged = future.result()
            divergence_map[i, j] = diverged

    return divergence_map

#tetration 계산
divergence_map = compute_tetration_divergence(n, max_iter, escape_radius)

if rot == "Y" or rot == "y":
    divergence_map = np.rot90(divergence_map, k=-1)

#plot
cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"]) # 커스텀 컬러맵 생성: 발산은 흰색, 수렴은 검은색
plt.imshow(divergence_map.T, extent=[x0 - eps, x0 + eps, y0 - eps, y0 + eps], origin='lower', cmap=cmap)
plt.axis('off')  # 축 라벨과 타이틀 제거
print(f"Complete")
filename = f"mytetration_{x0}_{y0}_{eps}_{n}.png"
plt.savefig(filename, dpi=600, bbox_inches='tight', pad_inches=0)
plt.show()


#pyinstaller --onefile PTF_user.py