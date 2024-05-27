import pyautogui
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#parameters - plot영역설정관련
x0 = float(pyautogui.prompt('x0 중심좌표를 입력하세요 (기본값: 0):   '))
y0 = float(pyautogui.prompt("y0 중심좌표를 입력하세요 (기본값: 0):   "))
eps = float(pyautogui.prompt("eps (x 축 범위)를 입력하세요 (기본값: 5e0):     ")) #x0 좌우로 eps만큼 plot함
eps_y = eps * (9/16)  # 9:16 비율에 맞추기 위해 y축 eps 계산
n = int(pyautogui.prompt("화소수를 입력하세요 (기본값: 500, 3840:4K, 1920:Full HD):     "))#화소수조절을 위한 parameter (3840:4K, 1920:Full HD)
nx, ny = n, int(n*(9/16)) #nx, ny : x,y축 화소수

#parameters - tetration계산 관련
max_iter = int(pyautogui.prompt("최대 반복 횟수 (max_iter)를 입력하세요 (기본값: 500):   ")) #최대 몇층까지 계산할 것인지를 정함. max_iter층 만큼 계산했는데 복소수 크기가 escape_radius를 벗어나지 않으면 수렴한것으로 처리.
escape_radius = float(pyautogui.prompt("발산 판단 기준 (escape_radius)를 입력하세요 (기본값: 1e+10):     "))
axis = float(pyautogui.prompt("축 라벨유뮤를 입력하세요 (1: 축라벨 포함 0: 축라벨 제거):     "))
#tetration 계산을 위한 함수설정
def compute_tetration_divergence(nx, ny, max_iter, escape_radius):
    x = np.linspace(x0 - eps, x0 + eps, nx)
    y = np.linspace(y0 - eps_y, y0 + eps_y, ny)
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
pyautogui.alert("오버플로우 경고가 뜨면 무시하시면 됩니다.\n 프로그램이 응답없음이 뜰수 있으며, 계산하는동안 창은 보이지 않습니다. \n 계속하시려면 확인을 클릭하세요")
#tetration 계산

divergence_map = compute_tetration_divergence(nx, ny, max_iter, escape_radius)
pyautogui.alert("모든 계산이 완료되었습니다. \n확인을 누르시면 결과를 보실수 있습니다!")


# plot
#plot
cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"]) # 커스텀 컬러맵 생성: 발산은 흰색, 수렴은 검은색
plt.imshow(divergence_map.T, extent=[x0 - eps, x0 + eps, y0 - eps_y, y0 + eps_y], origin='lower', cmap=cmap)
if axis <= 0:
    plt.axis('off')  # 축 라벨과 타이틀 제거
filename = f"mytetration_x_{x0}_y_{y0}_eps_{eps}.png"
plt.savefig(filename, dpi=600, bbox_inches='tight', pad_inches=0)
plt.show()
pyautogui.alert("계산된 결과가 저장되었습니다. \n파일 이름:   " + filename + "\n\n 확인을 누르시면 프로그램이 종료됩니다.") 