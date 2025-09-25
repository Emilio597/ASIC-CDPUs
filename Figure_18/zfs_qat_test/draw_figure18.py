import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

FONT_SIZE = 20
matplotlib.rcParams['pdf.fonttype'] = 42  # TrueType
matplotlib.rcParams['ps.fonttype'] = 42
# -------- 基础数据 --------
block_sizes = ['4K', '8K', '16K', '32K', '64K', '128K']
x = np.arange(len(block_sizes))

devices = ['OFF', 'Deflate(CPU)', 'QAT-8970', 'CSD 2000', 'DP-CSD']
colors  = ['#BB433E', '#D36C1D', '#E4C33F', '#A17C5B', '#1A7EC1']
markers = ['o', 's', '^', 'D', '*']   # ✅ 新 marker

latency_rd = [
    [86.3, 87.26, 87.2, 96.82, 111.2, 132.71],
    [86.06, 101.59, 129.63, 177.83, 266.88, 452.53],
    [87.06, 128.74, 153.71, 186.8, 231.01, 341.01],
    [174.97, 175.57, 220.73, 283.76, 374.34, 499.88],
    [85.71, 86.92, 92.31, 103.6, 136.62, 183.79],
]
latency_wr = [
    [4.72, 96.205, 99.576, 113.788, 142.043, 185.76],
    [5.99, 117.933, 147.253, 216.945, 343.849, 578.51],
    [5.34, 118.736, 139.716, 176.002, 240.685, 370.96],
    [5.88, 183.81, 221.4, 297.13, 404.01, 569.24],
    [5.01, 101.624, 104.254, 120.3, 168.377, 236.402],
]

# -------- 画图 --------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# (a) Read latency
for i in range(len(devices)):
    ax1.plot(x, latency_rd[i],
             color=colors[i], marker=markers[i],
             linewidth=6, markersize=15, label=devices[i])
ax1.set_ylabel("Latency (μs)", fontsize=FONT_SIZE)
ax1.set_xticks(x); ax1.set_xticklabels(block_sizes, fontsize=FONT_SIZE)
ax1.set_yticks(np.arange(0, 501, 100))
ax1.tick_params(axis='both', labelsize=FONT_SIZE)
ax1.grid(True, linestyle='--', alpha=.4)
ax1.text(0.5, -0.25, '(a) ZFS Read Latency',
         transform=ax1.transAxes, ha='center', fontsize=FONT_SIZE+2)

# (b) Write latency
for i in range(len(devices)):
    ax2.plot(x, latency_wr[i],
             color=colors[i], marker=markers[i],
             linewidth=6, markersize=15)
ax2.set_xticks(x); ax2.set_xticklabels(block_sizes, fontsize=FONT_SIZE)
ax2.set_yticks(np.arange(0, 601, 100))
ax2.tick_params(axis='both', labelsize=FONT_SIZE)
ax2.grid(True, linestyle='--', alpha=.4)
ax2.text(0.5, -0.25, '(b) ZFS Update Latency',
         transform=ax2.transAxes, ha='center', fontsize=FONT_SIZE+2)

# -------- Legend (线 + 点) --------
legend_elems = [
    Line2D([0], [0], color=colors[i], marker=markers[i],
           linewidth=3, markersize=10, label=devices[i])
    for i in range(len(devices))
]
fig.legend(handles=legend_elems, loc='upper center',
           bbox_to_anchor=(0.5, 1.05),
           ncol=len(devices), fontsize=FONT_SIZE-4,
           handlelength=3, handletextpad=0.8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("figs/zfs_rd_wr_latency.pdf", dpi=300, bbox_inches='tight')
plt.show()
