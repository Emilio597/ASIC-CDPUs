import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
import os

# ===== 确保保存路径存在 =====
os.makedirs("figs", exist_ok=True)

# ===== 设置字体与颜色 =====
FONT_SIZE = 24
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181']
markers = ['o', 's', 'D', '^']
labels_order = ['DPzip', 'DP-CSD', 'QAT 4XXX', 'QAT 8970']

# ===== 数据 =====
x_labels = ['100', '90', '80', '70', '60', '50', '40', '30', '20', '10', '0']
x_labels = x_labels[::-1]
x = np.arange(len(x_labels))

comp_data = {
    'DPzip': [13.5, 13.5, 13.5, 13.5, 13.5, 12.1, 11.4, 10.5, 13.5, 13.5, 13.5],
    'DP-CSD': [13.5, 13.5, 13.5, 13.4, 12.7, 11.4, 10.6, 9.81, 8.565, 8.096, 8.096],
    'QAT 4XXX': [7.32, 7.57, 8.04, 8.40, 8.78, 7.82, 7.19, 3.29, 3.16, 2.75, 2.45],
    'QAT 8970': [10.3157945, 10.17248724, 10.77086199, 9.897514246, 9.042210877, 8.516479284,
                 7.961061783, 7.473630831, 7.042428479, 6.658374332, 6.206915714]
}
decomp_data = {
    'DPzip': [13.9, 13.9, 13.9, 13.9, 13.9, 13.7, 12.5, 11.7, 13.2, 13.9, 13.9],
    'DP-CSD': [13.9, 13.9, 13.9, 13.9, 13.9, 13.8, 13.4, 11.8, 12.1, 13.9, 13.9],
    'QAT 4XXX': [23.59, 23.14, 21.14, 16.28, 13.13, 9.80, 9.30, 7.84, 6.67, 6.02, 5.21],
    'QAT 8970': [13.31674866, 13.31674866, 13.31674866, 13.07891216, 13.07891216,
                 13.07891216, 13.07891216, 13.07891216, 12.84945756, 12.84945756, 12.84945756]
}

# ===== 创建画布 =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(wspace=0.28, bottom=0.25, left=0.08, right=0.99, top=0.80)

# ===== 压缩 =====
for i, label in enumerate(labels_order):
    ax1.plot(x, comp_data[label], label=label, color=colors[i], marker=markers[i],
             linewidth=3, markersize=8)

ax1.set_xlabel("Compression Ratio(%)", fontsize=FONT_SIZE)
ax1.set_ylabel("Throughput (GB/s)", fontsize=FONT_SIZE)
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels, fontsize=18)
ax1.tick_params(axis='y', labelsize=FONT_SIZE)
ax1.yaxis.set_major_locator(MaxNLocator(nbins=6))
ax1.set_ylim(bottom=0)  # 👈 强制从 0 开始
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.text(0.5, -0.38, "(a) Compression", fontsize=FONT_SIZE,
         transform=ax1.transAxes, ha='center')

# ===== 解压缩 =====
for i, label in enumerate(labels_order):
    ax2.plot(x, decomp_data[label], label=label, color=colors[i], marker=markers[i],
             linewidth=3, markersize=8)

ax2.set_xlabel("Compression Ratio(%)", fontsize=FONT_SIZE)
ax2.set_xticks(x)
ax2.set_xticklabels(x_labels, fontsize=18)
ax2.tick_params(axis='y', labelsize=FONT_SIZE)
ax2.yaxis.set_major_locator(MaxNLocator(nbins=6))
ax2.set_ylim(bottom=0)  # 👈 强制从 0 开始
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.text(0.5, -0.38, "(b) Decompression", fontsize=FONT_SIZE,
         transform=ax2.transAxes, ha='center')

# ===== 图例 =====
handles = [plt.Line2D([0], [0], color=colors[i], marker=markers[i],
                      linewidth=3, markersize=8, label=labels_order[i])
           for i in range(len(labels_order))]
fig.legend(handles=handles,
           loc='upper center', bbox_to_anchor=(0.53, 0.92),
           fontsize=FONT_SIZE - 8, ncol=4, columnspacing=6.0, handletextpad=1.0)

# ===== 保存图像 =====
plt.savefig("bw_percentage.pdf", format="pdf", dpi=1200, bbox_inches="tight")
plt.show()
