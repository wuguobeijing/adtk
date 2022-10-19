import tkinter
import random
import tkinter as tk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from adtk.data import validate_series
from adtk.visualization import plot


from adtk.detector import SeasonalAD
seasonal_ad = SeasonalAD(c=3.0, side="both")
from adtk.detector import PcaAD
pca_ad = PcaAD(k=1)


def generate_data():
    global vacuum, efficiency, vacuumHisList, effiHisList
    vacuum = random.uniform(-1, 0)
    efficiency = random.uniform(30, 100)
    vacuumHisList.append(vacuum)
    effiHisList.append(efficiency)
    if len(vacuumHisList) > 15:
        vacuumHisList.pop(0)
        effiHisList.pop(0)

    root.after(1000, generate_data)


def generate_data2():
    global result, ts

    s = pd.read_csv('./data/seasonal.csv', index_col="Time", parse_dates=True, squeeze=True)
    s = validate_series(s)
    anomalies = seasonal_ad.fit_detect(s)
    df = pd.DataFrame(anomalies, columns=['Traffic'])
    df = df[ts:ts+100]
    df.rename(columns={'Time': 'Time', 'Traffic': 'label'}, inplace=True)
    df1 = pd.DataFrame(s, columns=['Traffic'])
    df1 = df1[ts:ts+100]
    result = pd.concat([df, df1], axis=1)
    ts += 5
    root.after(5000, generate_data2)


def generate_data3():
    global result_mul, ts
    s2 = pd.read_csv('./data/generator.csv', index_col="Time", parse_dates=True, squeeze=True)
    s2 = validate_series(s2)

    anomalies = pca_ad.fit_detect(s2)
    df2 = pd.DataFrame(anomalies, columns=['data'])
    df2 = df2[ts:ts+100]
    df1 = pd.DataFrame(s2, columns=['Speed (kRPM)', 'Power (kW)'])
    df1 = df1[ts:ts+100]
    result_mul = pd.concat([df2, df1], axis=1)
    ts += 5
    root.after(5000, generate_data3)


def plot_efffi_vacuum():
    global vacuum, efficiency, vacuumHisList, effiHisList, fig1

    fig1.clf()  # 清除上一帧内容

    g11 = fig1.add_subplot(2, 1, 1)
    g11.plot(vacuumHisList, effiHisList, c='lawngreen')
    g11.scatter(vacuum, efficiency, c="yellow", s=30)
    g11.set_xlim([-1, 1])
    g11.set_ylim([20, 100])
    g11.set_xlabel("vacuum bar")
    g11.set_ylabel("effi %")
    g11.patch.set_facecolor('whitesmoke')

    g12 = fig1.add_subplot(2, 1, 2)
    g12.set_xlim([0, 120])
    g12.set_ylim([-20, 20])
    g12.set_xlabel('time s')
    g12.set_ylabel('angle deg')
    g12.patch.set_facecolor('whitesmoke')

    canvas.draw()

    root.after(1000, plot_efffi_vacuum)


def plot_fpcurve():
    pass


def plot_vacuum():
    global fig2, result
    # global vacuum, efficiency, vacuumHisList, effiHisList, fig1
    fig2.clf()  # 清除上一帧内容

    g21 = fig2.add_subplot(2, 2, 1)

    g21.scatter(result.index, result['Traffic'], s=5, c=result['label'])
    g21.patch.set_facecolor('whitesmoke')
    canvas.draw()

    root.after(1000, plot_vacuum)


def plot_visor_angle():
    global fig3, result_mul
    # global vacuum, efficiency, vacuumHisList, effiHisList, fig1
    fig3.clf()  # 清除上一帧内容

    g21 = fig3.add_subplot(2, 2, 1)
    # g21.set_xlim([-1, 1])
    g21.set_ylim([0, 40])
    g21.plot(result_mul.index, result_mul['Speed (kRPM)'],linestyle='-', c='steelblue')
    g21.scatter(result_mul.index, result_mul['Power (kW)'], s=5, c=result_mul['data'])
    g21.patch.set_facecolor('whitesmoke')
    canvas.draw()

    root.after(1000, plot_visor_angle)


def write_spc_set(x, y):
    print(x, y)


def spc_set_window():
    spc_window = tk.Toplevel()
    spc_window.title("spc set")
    spc_window.geometry("250x200")

    label = tk.Label(spc_window, text="Kd: ", anchor='e')
    label.place(x=0, y=0, width=80, height=30)
    text = tk.Text(spc_window, font=tkFont.Font(size=16))
    text.tag_configure("tag_name", justify='center')
    text.place(x=80, y=0, width=100, height=30)

    label1 = tk.Label(spc_window, text="折算系数: ", anchor='e')
    label1.place(x=0, y=50, width=80, height=30)
    text1 = tk.Text(spc_window, font=tkFont.Font(size=16))
    text1.tag_configure("tag_name", justify='center')
    text1.place(x=80, y=50, width=100, height=30)

    spc_confirm_btn = tk.Button(spc_window, text="Confirm", font=tkFont.Font(size=16),
                                command=lambda: write_spc_set(text.get('0.0', 'end')[:-1],
                                                              text1.get('0.0', 'end')[
                                                              :-1]))  # 用lambda函数获取传入的参数，get 方法获取text中内容，-1去掉换行符
    spc_confirm_btn.place(x=80, y=100, width=100, height=30)


def avc_set_window():
    avc_window = tk.Toplevel()
    avc_window.title("avc set")
    avc_window.geometry("250x200")

    label = tk.Label(avc_window, text="真空高值: ", anchor='e')
    label.place(x=0, y=0, width=80, height=30)
    text = tk.Text(avc_window, font=tkFont.Font(size=16))
    text.tag_configure("tag_name", justify='center')
    text.place(x=80, y=0, width=100, height=30)

    label1 = tk.Label(avc_window, text="真空低值: ", anchor='e')
    label1.place(x=0, y=50, width=80, height=30)
    text1 = tk.Text(avc_window, font=tkFont.Font(size=16))
    text1.tag_configure("tag_name", justify='center')
    text1.place(x=80, y=50, width=100, height=30)

    spc_confirm_btn = tk.Button(avc_window, text="Confirm", font=tkFont.Font(size=16),
                                command=lambda: write_spc_set(text.get('0.0', 'end')[:-1],
                                                              text1.get('0.0', 'end')[
                                                              :-1]))  # 用lambda函数获取传入的参数，get 方法获取text中内容，-1去掉换行符
    spc_confirm_btn.place(x=80, y=100, width=100, height=30)


# 定义全局变量
vacuum = 0
efficiency = 0
ts = 0
vacuumHisList = []
effiHisList = []
result = pd.DataFrame
result_mul = pd.DataFrame

# 创建tkinter主界面
root = tk.Tk()
root.title("smart controller")
root.geometry("1800x1450+0+0")
root.configure(bg="gainsboro")
# 创建button
button_spc = tk.Button(root, text="spc设置", command=spc_set_window)
button_spc.place(x=0, y=0, width=100, height=30)
button_avc = tk.Button(root, text="avc设置", command=avc_set_window)
button_avc.place(x=100, y=0, width=100, height=30)

# 创建一个容器用于显示matplotlib的fig
frame1 = tk.Frame(root, bg="gainsboro")
frame1.place(x=0, y=30, width=3800, height=1600)
# 解决matplot中文显示乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 防止中文标签乱码，还有通过导入字体文件的方法
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['lines.linewidth'] = 1  # 设置曲线线条宽度
# 创建画图figure
fig1 = plt.figure(figsize=(4, 4))
fig1.subplots_adjust(left=0.15, right=0.9, top=0.95, bottom=0.15, wspace=0.5, hspace=0.5)
fig1.patch.set_facecolor('gainsboro')
g11 = fig1.add_subplot(2, 1, 1)
g11.set_xlim([-1, 1])
g11.set_ylim([20, 100])
g11.set_xlabel("vacuum bar")
g11.set_ylabel("effi %")
g11.patch.set_facecolor('whitesmoke')
g12 = fig1.add_subplot(2, 1, 2)
g12.set_xlim([0, 6])
g12.set_ylim([0, 4])
g12.set_xlabel('流量 m$^3$/s')
g12.set_ylabel('产量 m$^3$/s')
g12.patch.set_facecolor('whitesmoke')
# 将fig放入画布
canvas = FigureCanvasTkAgg(fig1, master=frame1)
canvas.draw()
# 将画布放进窗口
canvas.get_tk_widget().place(x=0, y=0)
# 创建第二个图
fig2 = plt.figure(figsize=(16, 8))
fig2.subplots_adjust(left=0.2, right=0.9, top=0.95, bottom=0.15, wspace=0.5, hspace=0.5)
fig2.patch.set_facecolor('gainsboro')
# g21 = fig2.add_subplot(2, 1, 1)
# g21.set_xlim([0, 120])
# g21.set_ylim([-1, 0])
# g21.set_xlabel("time s")
# g21.set_ylabel("vacuum bar")
# g21.patch.set_facecolor('whitesmoke')
# g22 = fig2.add_subplot(2, 1, 2)
# g22.set_xlim([0, 120])
# g22.set_ylim([-20, 20])
# g22.set_xlabel('time s')
# g22.set_ylabel('angle deg')
# g22.patch.set_facecolor('whitesmoke')

# fig2 放入画布
canvas2 = FigureCanvasTkAgg(fig2, master=frame1)
canvas2.draw()
canvas2.get_tk_widget().place(x=420, y=0)

fig3 = plt.figure(figsize=(16, 8))
fig3.subplots_adjust(left=0.4, right=0.9, top=0.95, bottom=0.15, wspace=0.5, hspace=0.5)
fig3.patch.set_facecolor('gainsboro')
# fig2 放入画布
canvas3 = FigureCanvasTkAgg(fig3, master=frame1)
canvas3.draw()
canvas3.get_tk_widget().place(x=320, y=200)
# 打开matplot交互模式
plt.ion()
# 使用一个定时器计算后台数据
generate_data()
generate_data2()
generate_data3()
# fig更新
plot_efffi_vacuum()
# plot_fpcurve()
plot_vacuum()
plot_visor_angle()

root.mainloop()