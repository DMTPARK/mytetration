import cupy as cp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm

# 파라미터 - 플롯 영역 설정
x0, y0 = -0.188427, 0.234446  # (x0, y0): 플롯 영역 중심 좌표
eps = 5e-3  # x0 좌우로 eps만큼 플롯함
eps_y = eps * (9/16)  # 16:9 비율에 맞추기 위해 y축 eps 계산
n = 1920  # 화소수 조절을 위한 파라미터 (1920: Full HD)
nx, ny = n, int(n * (9/16))  # nx, ny: x, y축 화소수

# 파라미터 - 테트레이션 계산 관련
max_iter = 500  # 최대 몇 층까지 계산할 것인지를 정함
escape_radius = 1e+10  # 복소수 크기가 escape_radius를 벗어나면 발산한 것으로 처리함

# 테트레이션 계산을 위한 함수 설정
def compute_tetration_divergence(nx, ny, max_iter, escape_radius, x0, y0, eps, eps_y):
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
        c[mask] = cp.nan  # 발산한 지점은 더 이상 계산하지 않음

    return divergence_map

# 플롯을 생성하는 함수
def plot_tetration(ax, x0, y0, eps, eps_y):
    divergence_map = compute_tetration_divergence(nx, ny, max_iter, escape_radius, x0, y0, eps, eps_y)
    cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"])
    ax.clear()
    img = ax.imshow(cp.asnumpy(divergence_map).T, extent=[x0 - eps, x0 + eps, y0 - eps_y, y0 + eps_y], origin='lower', cmap=cmap)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title(f"Tetration Plot at x={x0}, y={y0}, eps={eps}")
    plt.draw()
    plt.pause(0.01)  # 업데이트를 위해 잠시 대기

    return img

# 클릭 이벤트 핸들러
clicks = []
rect = None
cid = None

def on_click(event):
    global clicks, rect, cid
    if event.inaxes:
        if event.dblclick:  # 더블 클릭인 경우 아무 일도 하지 않음
            return
        clicks.append((event.xdata, event.ydata))
        if len(clicks) == 2:
            plt.gcf().canvas.mpl_disconnect(cid)
            plt.title("Calculating...")
            plt.draw()
            plt.gcf().canvas.flush_events()
            update_plot()
        elif len(clicks) == 1:
            rect = plt.Rectangle(clicks[0], 0, 0, linewidth=2, edgecolor='r', facecolor='none')  # 사각형 두께를 2로 변경
            event.inaxes.add_patch(rect)
            plt.draw()

def on_move(event):
    global rect
    if rect and len(clicks) == 1 and event.inaxes:
        x0, y0 = clicks[0]
        x1, y1 = event.xdata, event.ydata
        rect.set_width(x1 - x0)
        rect.set_height(y1 - y0)
        rect.set_xy((x0, y0))
        plt.draw()

def update_plot():
    global x0, y0, eps, eps_y, clicks, rect, cid
    (x1, y1), (x2, y2) = clicks
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    eps = abs(x2 - x1) / 2
    eps_y = abs(y2 - y1) / 2

    plt.title("Calculating...")  # 플롯 제목만 업데이트
    plot_tetration(ax, x0, y0, eps, eps_y)
    clicks = []
    rect = None
    cid = plt.gcf().canvas.mpl_connect('button_press_event', on_click)
    plt.gcf().canvas.mpl_connect('motion_notify_event', on_move)
    plt.title("Click two points to zoom in.")
    plt.draw()

# 초기 플롯 생성 및 사용자 인터랙션
fig, ax = plt.subplots()
plot_tetration(ax, x0, y0, eps, eps_y)
cid = plt.gcf().canvas.mpl_connect('button_press_event', on_click)
plt.gcf().canvas.mpl_connect('motion_notify_event', on_move)
plt.title("Click two points to zoom in.")
plt.show()
