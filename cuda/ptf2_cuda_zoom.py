import tkinter as tk
from tkinter import ttk
import cupy as cp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import threading
import time
import timeit


# 파라미터 - 플롯 영역 설정
x0, y0 = -0.188427, 0.234446  # (x0, y0): 플롯 영역 중심 좌표
eps = 5e-3  # x0 좌우로 eps만큼 플롯함
eps_y = eps * (9 / 16)  # 16:9 비율에 맞추기 위해 y축 eps 계산
eps_threshold = 1e-4 # 복소수 정밀도 임계값 설정
n = 1920  # 화소수 조절을 위한 파라미터 (1920: Full HD)
nx, ny = n, int(n * (9 / 16))  # nx, ny: x, y축 화소수

# 파라미터 - 테트레이션 계산 관련
max_iter = 500  # 최대 몇 층까지 계산할 것인지를 정함
escape_radius = 1e+10  # 복소수 크기가 escape_radius를 벗어나면 발산한 것으로 처리함

# 테트레이션 계산을 위한 함수 설정
def compute_tetration_divergence(nx, ny, max_iter, escape_radius, x0, y0, eps, eps_y, progress_callback=None):
    # Start timer to measure total execution time
    start_time = timeit.default_timer()

    x = cp.linspace(x0 - eps, x0 + eps, nx)
    y = cp.linspace(y0 - eps_y, y0 + eps_y, ny)

    # Determine complex number data type based on precision threshold
    dtype = cp.complex64 if eps >= eps_threshold else cp.complex128

    # c, z 배열 데이터 생성 및 반환
    c = cp.array(x[:, cp.newaxis] + 1j * y[cp.newaxis, :], dtype=dtype)
    z = cp.empty(c.shape, dtype=dtype)

    z[:] = c

    divergence_map = cp.zeros(c.shape, dtype=cp.bool_)
    update_frequency = max_iter // 10  # Progress bar 10% 단위로 업데이트

    for i in range(max_iter):
        cp.power(c, z, out=z)
        mask = cp.abs(z) > escape_radius
        divergence_map[mask] = True
        c[mask] = cp.nan  # 발산한 지점은 더 이상 계산하지 않음

        # Progressbar 업데이트 (update_frequency 비율로 호출됨)
        if progress_callback and (i % update_frequency == 0 or i == max_iter - 1):
            progress_callback(i + 1, max_iter)

    # Stop timer and calculate total execution time (콘솔창 확인용)
    end_time = timeit.default_timer()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")

    return divergence_map

# 플롯을 생성하는 함수
def plot_tetration(app, ax, x0, y0, eps, eps_y):
    # 프로그래스 바 진행상황 갱신  "Time: 남은시간 / 예상 총 소요시간, Progress: 진행률%" 
    start_time = time.time()
    def progress_callback(current, total):
        progress = (current / total) * 100
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / current) * total if current > 0 else 0
        remaining_time = estimated_total_time - elapsed_time
        iterations_per_second = current / elapsed_time if elapsed_time > 0 else 0
        time_info = f"Time: {remaining_time:.2f}s / Estimated total: {estimated_total_time:.2f}s, Progress: {progress:.2f}%, Speed: {iterations_per_second:.2f} it./s"
        app.status_label.config(text=f"Calculating... {time_info}")
        app.progress["value"] = progress
        app.root.update_idletasks()

    app.set_calculation_status(True)  # 계산이 시작되었음을 알림
    divergence_map = compute_tetration_divergence(nx, ny, max_iter, escape_radius, x0, y0, eps, eps_y, progress_callback)

    cmap = LinearSegmentedColormap.from_list("custom_cmap", ["black", "white"])
    norm = plt.Normalize(vmin=0, vmax=1) # 플롯 전체가 white 일때, 전체가 black 으로 표현되는 증상 해결

    ax.clear()
    ax.imshow(cp.asnumpy(divergence_map).T, extent=[x0 - eps, x0 + eps, y0 - eps_y, y0 + eps_y], origin='lower', cmap=cmap, norm=norm)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title(f"Tetration Plot at x={x0}, y={y0}, eps={eps}")
    ax.set_autoscale_on(False)  # 자동 축 조정 비활성화
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=True))
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=True))
    app.set_calculation_status(False)  # 계산이 완료되었음을 알림
    app.progress["value"] = 0  # 계산이 끝난 후 Progressbar 초기화

# 클릭 이벤트 핸들러
clicks = []
rect = None

def on_click(event, app):
    global clicks, rect
    if event.inaxes == app.ax:
        clicks.append((event.xdata, event.ydata))
        if len(clicks) == 2:
            app.status_label.config(text="Calculating...")
            app.update_plot()
        elif len(clicks) == 1:
            rect = app.ax.add_patch(plt.Rectangle(clicks[0], 0, 0, linewidth=2, edgecolor='r', facecolor='none'))
            app.canvas.draw()

def on_move(event, app):
    global rect
    if rect and len(clicks) == 1 and event.inaxes == app.ax:
        x0, y0 = clicks[0]
        x1, y1 = event.xdata, event.ydata
        rect.set_width(x1 - x0)
        rect.set_height(y1 - y0)
        rect.set_xy((x0, y0))
        app.canvas.draw()

class ZoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoom Application")
        self.calculation_in_progress = False

        self.invert_zoom = tk.BooleanVar(value=False)

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar_frame = tk.Frame(self.root)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        self.zoom_out_label = ttk.Label(self.toolbar_frame, text="Zoom Out: ")
        self.zoom_out_label.pack(side=tk.LEFT)

        self.invert_zoom_checkbox = ttk.Checkbutton(self.toolbar_frame, text="Invert Zoom", variable=self.invert_zoom, command=self.toggle_invert_zoom)
        self.invert_zoom_checkbox.pack(side=tk.LEFT)

        self.zoom_factors = [10, 100, 1000, 10000, 100000]
        self.buttons = []
        for factor in self.zoom_factors:
            button = ttk.Button(self.toolbar_frame, text=f"1/{factor}", command=lambda f=factor: self.zoom(f))
            button.pack(side=tk.LEFT)
            self.buttons.append(button)

        self.status_label = tk.Label(self.root, text="Program Status: Ready")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(self.controls_frame, text="X:").pack(side=tk.LEFT)
        self.x_entry = ttk.Entry(self.controls_frame)
        self.x_entry.pack(side=tk.LEFT)

        tk.Label(self.controls_frame, text="Y:").pack(side=tk.LEFT)
        self.y_entry = ttk.Entry(self.controls_frame)
        self.y_entry.pack(side=tk.LEFT)

        tk.Label(self.controls_frame, text="Eps:").pack(side=tk.LEFT)
        self.eps_entry = ttk.Entry(self.controls_frame, width=25)
        self.eps_entry.pack(side=tk.LEFT)

        self.apply_button = ttk.Button(self.controls_frame, text="Apply", command=self.update_plot_from_entry)
        self.apply_button.pack(side=tk.LEFT)

        self.copy_button = ttk.Button(self.controls_frame, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT)

        self.cid_click = self.canvas.mpl_connect('button_press_event', lambda event: on_click(event, self))
        self.cid_move = self.canvas.mpl_connect('motion_notify_event', lambda event: on_move(event, self))

        self.current_x0 = x0
        self.current_y0 = y0
        self.current_eps = eps

        self.plot_initial()

    def set_calculation_status(self, status, message=None):
        self.calculation_in_progress = status
        if status:
            self.status_label.config(text="Calculating...")
        else:
            if message is not None:
                self.status_label.config(text=message)
            else:
                self.status_label.config(text="Click two points to Zoom In.")

    def plot_initial(self):
        threading.Thread(target=self.update_plot_with_thread, args=(x0, y0, eps, eps_y)).start()

    def toggle_invert_zoom(self):
        if self.invert_zoom.get():
            self.zoom_out_label.config(text="Zoom In: ")
            for i, factor in enumerate(self.zoom_factors):
                self.buttons[i].config(text=str(factor))
        else:
            self.zoom_out_label.config(text="Zoom Out: ")
            for i, factor in enumerate(self.zoom_factors):
                self.buttons[i].config(text=f"1/{factor}")

    def zoom(self, factor):
        self.set_calculation_status(True)
        self.progress["value"] = 0
        global x0, y0, eps, eps_y
        if self.invert_zoom.get():
            # Zoom In을 위해 빨간 사각형 표시
            new_eps = eps / factor
            new_eps_y = eps_y / factor
            rect = plt.Rectangle((x0 - new_eps, y0 - new_eps_y), 2 * new_eps, 2 * new_eps_y, linewidth=2, edgecolor='r', facecolor='none')
            self.ax.add_patch(rect)
            self.canvas.draw()

            eps = new_eps
            eps_y = new_eps_y
        else:
            eps *= factor
            eps_y *= factor

        threading.Thread(target=self.update_plot_with_thread, args=(x0, y0, eps, eps_y)).start()

    def update_entries(self):
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(tk.END, str(x0))
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(tk.END, str(y0))
        self.eps_entry.delete(0, tk.END)
        self.eps_entry.insert(tk.END, str(eps))

    def update_plot_from_entry(self):
        self.set_calculation_status(True, "Calculation in progress...(update_plot_from_entry)")
        self.progress["value"] = 0
        self.canvas.draw()
        global x0, y0, eps, eps_y
        try:
            new_x0 = float(self.x_entry.get())
            new_y0 = float(self.y_entry.get())
            new_eps = float(self.eps_entry.get())
            if (new_x0, new_y0, new_eps) == (self.current_x0, self.current_y0, self.current_eps):
                self.status_label.config(text="Parameters are the same. No need to update.")
                return
            x0, y0, eps = new_x0, new_y0, new_eps
            eps_y = eps * (9 / 16)
            threading.Thread(target=self.update_plot_with_thread, args=(x0, y0, eps, eps_y)).start()
            self.current_x0 = x0
            self.current_y0 = y0
            self.current_eps = eps
        except ValueError as error:
            print("Error:", error)
            self.status_label.config(text="Invalid input. Please enter valid numbers.")

    def update_plot(self):
        self.set_calculation_status(True, "Calculation in progress...(update_plot)")
        self.progress["value"] = 0
        self.canvas.draw()
        global x0, y0, eps, eps_y, clicks, rect
        (x1, y1), (x2, y2) = clicks
        x0 = (x1 + x2) / 2
        y0 = (y1 + y2) / 2
        eps = abs(x2 - x1) / 2
        eps_y = abs(y2 - y1) / 2
        threading.Thread(target=self.update_plot_with_thread, args=(x0, y0, eps, eps_y)).start()
        clicks = []
        rect = None
        self.update_entries()
        self.current_x0 = x0
        self.current_y0 = y0
        self.current_eps = eps

    def update_plot_with_thread(self, x0, y0, eps, eps_y):
        plot_tetration(self, self.ax, x0, y0, eps, eps_y)
        self.set_calculation_status(False)
        self.status_label.config(text="Click two points to Zoom In.")
        self.canvas.draw()

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(f"x={x0}, y={y0}, eps={eps}")
        self.status_label.config(text="Copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZoomApp(root)
    root.mainloop()
