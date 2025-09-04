import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

# ===== 全局设置 =====
FONT_SIZE = 24
devices = ['OFF', 'Deflate(CPU)', 'QAT 8970', 'QAT 4XXX', 'CSD 2000', 'DP-CSD']
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#A17C5B', '#1A7EC1']
markers = ['o', '^', 's', 'D', 'v', '*']
processes = [10, 20, 30, 40, 50, 60, 70, 80, 88]

def to_k(x, _): return f"{x / 1000:.1f}K"

# ===== Power Efficiency 数据（Workload A）=====
power_eff_A = {
    "OFF": [4708.59, 5203.83, 5704.35, 5110.93, 5140.35, 5239.63, 4956.23, 4868.06, 5517.59],
    "CPU": [1658.96, 1805.86, 1829.14, 2068.88, 2166.47, 2695.03, 3037.95, 3432.74, 3419.59],
    "QAT 8970": [2136.72, 2210.74, 2520.65, 2625.85, 2750.74, 2929.98, 2825.02, 2795.50, 2728.45],
    "QAT 4XXX": [3302.43, 3383.55, 3428.64, 3649.49, 3791.26, 3761.05, 3578.32, 3467.46, 3354.95],
    "CSD 2000": [1181.77, 2450.05, 2213.15, 2494.71, 3030.51, 2878.17, 2913.55, 2116.60, 1726.24],
    "CSD": [4103.53, 4465.29, 5224.40, 4920.06, 5138.32, 5060.30, 4777.69, 4811.23, 5056.46],
}

# ===== Power Efficiency 数据（Workload B）=====
power_eff_B = {
    "OFF": [4176.50, 4983.59, 5212.69, 5032.07, 4889.70, 4478.41, 4886.67, 5059.69, 5066.02],
    "CPU": [1315.64, 1502.12, 1813.41, 2036.17, 2398.19, 2671.61, 3059.85, 3205.34, 3250.42],
    "QAT 8970": [1956.81, 2055.93, 2292.33, 2525.91, 2741.11, 2846.21, 2765.28, 2765.42, 2680.55],
    "QAT 4xxx": [3155.98, 3305.61, 3435.53, 3618.68, 3757.70, 3796.55, 3521.17, 3348.46, 3221.64],
    "CSD 2000": [1302.34, 2372.53, 2217.34, 2918.27, 2843.21, 2817.59, 2557.57, 2138.40, 1633.01],
    "CSD": [3948.33, 4791.80, 4996.20, 4774.75, 4764.30, 4396.92, 4856.84, 4942.86, 4881.73],
}

# ===== 创建共享 y 轴的图形 =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
plt.subplots_adjust(wspace=0.15, top=0.80, bottom=0.26)

# ---- (a) Power Efficiency (Workload A) ----
ax1.set_ylabel('Pwr Eff. (OPs/Joule)', fontsize=FONT_SIZE)
ax1.set_xlabel('Number of Processes\n(a) Workload A', fontsize=FONT_SIZE, labelpad=20)
ax1.set_xticks(np.arange(0, 101, 25))
ax1.tick_params(axis='both', labelsize=FONT_SIZE)
ax1.set_ylim(0, 6000)
ax1.yaxis.set_major_formatter(FuncFormatter(to_k))
for idx, (label, vals) in enumerate(power_eff_A.items()):
    ax1.plot(processes, vals, label=label, marker=markers[idx],
             color=colors[idx], linewidth=5, markersize=10)
ax1.grid(True)

# ---- (b) Power Efficiency (Workload B) ----
ax2.set_xlabel('Number of Processes\n(b) Workload F', fontsize=FONT_SIZE, labelpad=20)
ax2.set_xticks(np.arange(0, 101, 25))
ax2.tick_params(axis='both', labelsize=FONT_SIZE)
ax2.yaxis.set_major_formatter(FuncFormatter(to_k))
for idx, (label, vals) in enumerate(power_eff_B.items()):
    ax2.plot(processes, vals, label=label, marker=markers[idx],
             color=colors[idx], linewidth=5, markersize=10)
ax2.grid(True)

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
           fontsize=FONT_SIZE - 8,
           loc='upper center',
           bbox_to_anchor=(0.5, 1.0),
           ncol=3,
           columnspacing=6.0,
           handletextpad=1.0,
           handlelength=3.0)

# ---- 保存与展示 ----
plt.savefig("figs/ycsb-powereff.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
