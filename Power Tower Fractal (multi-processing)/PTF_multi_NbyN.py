import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.colors import LinearSegmentedColormap
import multiprocessing as mp

#parameters - plot 영역 설정 관련
x0 = 0
y0 = 0 #(x0,y0) : plot 영역 중심좌표
eps = 5e1 #x0 좌우로 eps만큼 plot함
n = 400 #화소수 조절을 위한 parameter (3840: 대략 4K 화질, 1920: Full HD 화질)

#parameters - tetration 계산 관련
max_iter = 500 #최대 몇층까지 계산할 것인지를 정함. max_iter 층만큼 계산했는데 복소수 크기가 escape_radius를 벗어나지 않으면 수렴한 것으로 처리.
escape_radius = 1e+10 #복소수 크기가 escape_radius를 벗어나면 발산한 것으로 처리함.

# 한 열에 대한 테트레이션 발산 계산 함수
def compute_column(j, x, y, max_iter, escape_radius):
    c_val_col = x[j] + 1j * y
    divergence_col = np.zeros_like(c_val_col, dtype=bool)

    for i in range(len(y)):
        c_val = c_val_col[i]
        z = c_val
        for k in range(max_iter):
            z = c_val ** z
            if np.abs(z) > escape_radius:
                divergence_col[i] = True
                break

    return divergence_col

def compute_tetration_divergence_parallel(n, max_iter, escape_radius):
    x = np.linspace(x0 - eps, x0 + eps, n)
    y = np.linspace(y0 - eps, y0 + eps, n)
    divergence_map = np.zeros((n, n), dtype=bool)

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = [pool.apply_async(compute_column, args=(j, x, y, max_iter, escape_radius)) for j in range(n)]
        for j, result in tqdm(enumerate(results), total=n, mininterval=1):
            divergence_map[j, :] = result.get()

    return divergence_map

def main():
    # 테트레이션 계산
    divergence_map = compute_tetration_divergence_parallel(n, max_iter, escape_radius)

    # plot
    cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"])  # 커스텀 컬러맵 생성: 발산은 흰색, 수렴은 검은색
    plt.imshow(divergence_map.T, extent=[x0 - eps, x0 + eps, y0 - eps, y0 + eps], origin='lower', cmap=cmap)
    plt.axis('off')  # 축 라벨과 타이틀 제거
    filename = f"mytetration_x_{x0}_y_{y0}_eps_{eps}.png"
    plt.savefig(filename, dpi=600, bbox_inches='tight', pad_inches=0)
    plt.show()

if __name__ == "__main__":
    main()