import cupy as cp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm

# 파라미터 - 플롯 영역 설정
x0 = -0.188427
y0 = 0.234446  # (x0,y0) : 플롯 영역 중심 좌표
eps = 5e-3  # x0 좌우로 eps만큼 플롯함
eps_y = eps * (9/16)  # 16:9 비율에 맞추기 위해 y축 eps 계산
n = 1920  # 화소수 조절을 위한 파라미터 (3840:4K, 1920:Full HD)
nx, ny = n, int(n * (9/16))  # nx, ny : x, y축 화소수

# 파라미터 - 테트레이션 계산 관련
max_iter = 500  # 최대 몇 층까지 계산할 것인지를 정함
escape_radius = 1e+10  # 복소수 크기가 escape_radius를 벗어나면 발산한 것으로 처리함

# 테트레이션 계산을 위한 함수 설정
def compute_tetration_divergence(nx, ny, max_iter, escape_radius):
    x = cp.linspace(x0 - eps, x0 + eps, nx)
    y = cp.linspace(y0 - eps_y, y0 + eps_y, ny)
    c = x[:, cp.newaxis] + 1j * y[cp.newaxis, :]
    z = cp.empty_like(c)
    z[:] = c

    divergence_map = cp.zeros(c.shape, dtype=cp.bool_)

    for k in tqdm(range(max_iter), desc="Calculating Tetration", ncols=100):
        cp.power(c, z, out=z)
        mask = cp.abs(z) > escape_radius
        divergence_map[mask] = True
        c[mask] = cp.nan  # Escape from further computation for diverged points

    return divergence_map

# 테트레이션 계산
divergence_map = compute_tetration_divergence(nx, ny, max_iter, escape_radius)

# 플롯
cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"])  # 커스텀 컬러맵 생성
plt.imshow(cp.asnumpy(divergence_map).T, extent=[x0 - eps, x0 + eps, y0 - eps_y, y0 + eps_y], origin='lower', cmap=cmap)
plt.axis('off')  # 축 라벨과 타이틀 제거
filename = f"mytetration_x_{x0}_y_{y0}_eps_{eps}.png"
plt.savefig(filename, dpi=600, bbox_inches='tight', pad_inches=0)
plt.show()
