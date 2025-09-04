import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

# ===== 全局设置 =====
FONT_SIZE = 22
devices = ['OFF', 'Deflate(CPU)', 'QAT 8970', 'QAT 4XXX', 'CSD 2000', 'DP-CSD']
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#A17C5B', '#1A7EC1']
markers = ['o', '^', 's', 'D', 'v', '*']
processes = [10, 20, 30, 40, 50, 60, 70, 80, 88]

def to_k(x, _): return f"{x / 1000000:.1f}M"

# ===== Power Efficiency 数据（Workload A）=====
power_eff_A = {
    "OFF":       [226012.42, 423956.44, 609851.82, 727591.51, 909841.14, 973417.67, 970627.37, 972004.98, 1112015.94],
    "CPU":       [106339.62, 210365.07, 310423.68, 410548.67, 503639.88, 625247.37, 720904.49, 777960.81, 799055.18],
    "QAT 8970":  [196578.28, 287396.05, 383139.04, 525170.77, 594159.52, 650455.16, 667325.34, 665439.92, 665958.92],
    "QAT 4XXX":  [277404.53, 485098.96, 626961.40, 706686.96, 748925.63, 760635.66, 766404.52, 767313.97, 763853.99],
    "CSD 2000":  [148902.67, 350357.48, 413858.12, 548837.19, 624285.91, 615927.63, 617671.64, 444486.01, 355605.4],
    "DP-CSD":    [214860.67, 408573.69, 564235.72, 700075.53, 874438.93, 918444.51, 997151.97, 957193.77, 1040871.98],
}

# ===== Power Efficiency 数据（Workload B）=====
power_eff_B = {
    "OFF":       [214379.84, 391211.64, 560363.66, 660056.18, 821470.22, 853674.67, 938240.81, 1040576.33, 1053731.62],
    "CPU":       [104119.99, 207066.64, 306247.95, 399089.69, 518775.42, 601539.53, 705692.80, 754632.97, 779221.99],
    "QAT 8970":  [189889.06, 280737.39, 380113.50, 517079.15, 579745.53, 638433.21, 653214.11, 658280.43, 654269.36],
    "QAT 4XXX":  [262735.48, 465561.84, 609016.72, 682626.93, 740153.75, 752361.68, 760573.45, 759799.71, 759951.60],
    "CSD 2000":  [147164.30, 344016.25, 447902.45, 542799.08, 594230.43, 619869.37, 560107.67, 470448.71, 360896.16],
    "DP-CSD":    [203931.39, 381618.57, 525750.54, 628165.63, 798449.69, 834622.73, 904295.56, 1008343.91, 1018182.32],
}

# ===== 创建共享 y 轴的图形 =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
plt.subplots_adjust(wspace=0.15, top=0.80, bottom=0.26)

# ---- (a) Power Efficiency (Workload A) ----
ax1.set_ylabel('Throughput (OPS)', fontsize=FONT_SIZE)
ax1.set_xlabel('Number of Processes', fontsize=FONT_SIZE)
ax1.set_xticks(np.arange(0, 101, 25))
ax1.tick_params(axis='both', labelsize=FONT_SIZE)
ax1.yaxis.set_major_formatter(FuncFormatter(to_k))
for idx, (label, vals) in enumerate(power_eff_A.items()):
    ax1.plot(processes, vals, label=label, marker=markers[idx],
             color=colors[idx], linewidth=4, markersize=10)
ax1.grid(True)
ax1.text(0.5, -0.40, "(a) Workload A", transform=ax1.transAxes, ha='center', fontsize=FONT_SIZE)

# ---- (b) Power Efficiency (Workload B) ----
ax2.set_xlabel('Number of Processes', fontsize=FONT_SIZE)
ax2.set_xticks(np.arange(0, 101, 25))
ax2.tick_params(axis='both', labelsize=FONT_SIZE)
ax2.yaxis.set_major_formatter(FuncFormatter(to_k))
for idx, (label, vals) in enumerate(power_eff_B.items()):
    ax2.plot(processes, vals, label=label, marker=markers[idx],
             color=colors[idx], linewidth=4, markersize=10)
ax2.grid(True)
ax2.text(0.5, -0.40, "(b) Workload F", transform=ax2.transAxes, ha='center', fontsize=FONT_SIZE)

# ---- 图例（线 + 点）----
legend_elements = [
    Line2D([0], [0],
           color=colors[i],
           marker=markers[i],
           label=devices[i],
           linewidth=3,
           markersize=10,
           markerfacecolor=colors[i],
           markeredgecolor='black',
           linestyle='-')
    for i in range(len(devices))
]
fig.legend(legend_elements,
           devices,
           fontsize=FONT_SIZE - 4,
           loc='upper center',
           bbox_to_anchor=(0.5, 1.0),
           ncol=3,
           columnspacing=6.0,
           handletextpad=1.0,
           handlelength=3.0)

# ---- 保存与展示 ----
plt.savefig("figs/ycsb-throughput.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
