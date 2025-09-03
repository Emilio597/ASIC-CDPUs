import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# 统一风格参数
FONT_SIZE = 12
FIG_SIZE = (7.2, 2.8)
BAR_WIDTH = 0.25
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#1A7EC1', '#429EBD']

# 数据 - 左图（折线图）
block_sizes_line = ['1k', '2k', '4k', '8k', '16k', '32k', '64k']
#avg_read_latency = [354, 364, 414, 462, 420, 436, 448]  # 原始读延迟
#avg_read_latency_llc_miss = [9529,9787,10237,11696,15840,20320,31440]  # LLC miss 时的延迟，对应从4k开始

avg_read_latency = [x / 1000 for x in [354, 364, 414, 462, 420, 436, 448]]
avg_read_latency_llc_miss = [x / 1000 for x in [9529,9787,10237,11696,15840,20320,31440]]

# 创建并排的两个子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_SIZE)

### 左图：折线图
ax1.plot(block_sizes_line, avg_read_latency, color=colors[0], marker='o', linewidth=2, markersize=5, alpha=0.5, label="Read Latency")
ax1.plot(block_sizes_line, avg_read_latency_llc_miss, color=colors[1], marker='s', linewidth=2, markersize=5, alpha=0.5, label="Read Latency (LLC miss)")

ax1.set_ylabel('Latency (µs)', fontsize=FONT_SIZE+2)
ax1.set_xlabel('Chunk Size\n(a) Read Latency', fontsize=FONT_SIZE+2)
ax1.set_ylim(0, 35)
ax1.tick_params(axis='both', labelsize=FONT_SIZE+2)
ax1.yaxis.set_major_locator(MaxNLocator(nbins=6))
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# 添加标签
for x, y in zip(block_sizes_line, avg_read_latency):
    ax1.text(x, y + 0.5, f'{y:.2f}', ha='center', va='bottom', fontsize=FONT_SIZE - 1)

for x, y in zip(block_sizes_line, avg_read_latency_llc_miss):
    ax1.text(x, y + 0.5, f'{y:.2f}', ha='center', va='bottom', fontsize=FONT_SIZE - 1)

### 右图：堆叠柱状图
block_sizes_bar = ['16k', '32k', '64k']
comp_read = [0.42, 0.436, 0.448]
comp_write = [14.706, 20.936, 33.190]
comp_read_rw = [15.84, 20.32, 31.44]
comp_write_rw = [44.16, 79.68, 153.56]

x = np.arange(len(block_sizes_bar))
# 无干扰
ax2.bar(x - BAR_WIDTH / 2, comp_write, BAR_WIDTH, color=colors[0], edgecolor='black', alpha=1)
ax2.bar(x - BAR_WIDTH / 2, comp_read, BAR_WIDTH, bottom=comp_write, color=colors[0], edgecolor='black', alpha=0.5)
# 有干扰
ax2.bar(x + BAR_WIDTH / 2, comp_write_rw, BAR_WIDTH, color=colors[1], edgecolor='black', alpha=1)
ax2.bar(x + BAR_WIDTH / 2, comp_read_rw, BAR_WIDTH, bottom=comp_write_rw, color=colors[1], edgecolor='black', alpha=0.5)

ax2.set_xticks(x)
ax2.set_xticklabels(block_sizes_bar, fontsize=FONT_SIZE+2)
ax2.set_ylabel('Latency (µs)', fontsize=FONT_SIZE+2)
ax2.set_xlabel('Chunk Size\n(b) End-to-end latency', fontsize=FONT_SIZE+2)
ax2.tick_params(axis='y', labelsize=FONT_SIZE)
ax2.grid(axis='y', linestyle='--', alpha=0.4)

# 图例统一放上面居中
handles = [
    # 左图：折线
    plt.Line2D([0], [0], color=colors[0], marker='o', linewidth=2, alpha=0.5, label='4XXX'),
    plt.Line2D([0], [0], color=colors[1], marker='s', linewidth=2, alpha=0.5, label='8970 (Est.)'),

    # 右图：堆叠柱
    plt.Rectangle((0, 0), 1, 1, color=colors[0], alpha=1, edgecolor='black', label='4XXX Comp+Write'),
    plt.Rectangle((0, 0), 1, 1, color=colors[0], alpha=0.4, edgecolor='black', label='4XXX Read'),
    plt.Rectangle((0, 0), 1, 1, color=colors[1], alpha=1, edgecolor='black', label='8970 Comp+Write (Est.)'),
    plt.Rectangle((0, 0), 1, 1, color=colors[1], alpha=0.4, edgecolor='black', label='8970 Read (Est.)'),
]
fig.legend(handles, [h.get_label() for h in handles], fontsize=FONT_SIZE, loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3)

plt.tight_layout()
plt.savefig("combined_latency_fig.pdf", format="pdf", bbox_inches="tight", dpi=1200)
plt.show()
