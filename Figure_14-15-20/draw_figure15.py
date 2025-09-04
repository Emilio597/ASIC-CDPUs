import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# ===== 设置 =====
FONT_SIZE = 24
devices = ['OFF', 'Deflate(CPU)', 'QAT 8970', 'QAT 4XXX', 'CSD 2000', 'DP-CSD']
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#A17C5B', '#1A7EC1']
bar_width = 0.15
group_gap = 0.1
x_groups = [0, 1 + group_gap]
offsets = (np.arange(6) - 2.5) * bar_width  # align for 6 devices
x_write = x_groups[0] + offsets
x_read = x_groups[1] + offsets
x_all = np.concatenate([x_write, x_read])
bar_colors = colors[:6] * 2

def to_k(x, _): return f"{x / 1000:.1f}K"

# ===== 数据 =====
latency_read_A = [1062.18, 1420.88, 875.92, 849.42, 2559.69, 1114.59]
# latency_write_A = [1069.7, 1453.77, 857.75, 864.9, 2582.6, 1134.46]
# latency_A = latency_read_A + latency_write_A

latency_read_B = [1284.38, 1573.32, 853.09, 744.26, 2046.08, 1095.25]
# latency_write_B = [50, 47.34, 31.25, 35.79, 51.09, 44.11]
# latency_B = latency_read_B + latency_write_B
latency_AB = latency_read_A + latency_read_B

# ===== 图形绘制 =====
fig, ax1 = plt.subplots(1, 1, figsize=(7, 5))
plt.subplots_adjust(wspace=0.15, top=0.80, bottom=0.26)

# ---- (a) Workload A ----
ax1.set_ylabel("Latency (μs)", fontsize=FONT_SIZE)
ax1.set_xlabel("Read Latency", fontsize=FONT_SIZE, labelpad=20)
ax1.tick_params(axis='y', labelsize=FONT_SIZE)
ax1.yaxis.set_major_formatter(FuncFormatter(to_k))
for i, x in enumerate(x_all):
    ax1.bar(x, latency_AB[i], width=bar_width, color=bar_colors[i], edgecolor='black')
ax1.set_xticks([])
ax1.set_xticks(x_groups, minor=True)
ax1.set_xticklabels(['Workload A', 'Workload F'], minor=True, fontsize=FONT_SIZE)
ax1.tick_params(axis='x', which='minor')

# # ---- (b) Workload B ----
# ax2.set_xlabel("(b) Workload F", fontsize=FONT_SIZE, labelpad=20)
# ax2.tick_params(axis='y', labelsize=FONT_SIZE)
# ax2.yaxis.set_major_formatter(FuncFormatter(to_k))
# for i, x in enumerate(x_all):
#     ax2.bar(x, latency_B[i], width=bar_width, color=bar_colors[i], edgecolor='black')
# ax2.set_xticks([])
# ax2.set_xticks(x_groups, minor=True)
# ax2.set_xticklabels(['Read', 'Update'], minor=True, fontsize=FONT_SIZE)
# ax2.tick_params(axis='x', which='minor')

# ===== 图例 =====
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i], edgecolor='black') for i in range(len(devices))]
fig.legend(handles, devices,
           fontsize=FONT_SIZE - 8,
           loc='upper center',
           bbox_to_anchor=(0.5, 1.0),
           ncol=3,
        #    columnspacing=6.0,
           handletextpad=1.0)

# ===== 保存与展示 =====
plt.savefig("figs/ycsb-lat.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.show()
