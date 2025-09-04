import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

FONT_SIZE = 20

## 统一设置
devices = ['OFF', 'Deflate(CPU)', 'QAT 8970', 'QAT 4XXX', 'DP-CSD', 'CSD2000']
#colors = ['#DD514C', '#F37B1D', '#FAD232', '#5EB95E', '#1F8DD6', '#8058A5']
#colors = ['#DD514C', '#F37B1D', '#FAD232', '#5EB95E', '#8058A5']
#dark version
#colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#1A7EC1', '#429EBD']
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#429EBD', '#A17C5B']
num_devices = len(devices)
bar_width = 0.15
group_gap = 0.1
x_groups = [0, 1 + group_gap]
offsets = (np.arange(num_devices) - (num_devices - 1)/2) * bar_width

## ====================== 数据 ======================
# write_perf = [9646, 1936, 2756, 2617, 1673]
# read_perf = [13619, 3924, 3964, 4515, 13516]

write_perf = [5230, 1936, 2444, 2815, 4651, 2263]
read_perf = [10547.2, 3924, 6805, 7810, 10158.1, 2781]


perf_all = write_perf + read_perf
x_write_perf = x_groups[0] + offsets
x_read_perf = x_groups[1] + offsets
x_all_perf = np.concatenate([x_write_perf, x_read_perf])
bar_colors_perf = colors * 2

# write_lat = [158, 204, 203, 204, 159]
# read_lat = [57, 572, 236, 151, 63]

write_lat = [156, 204, 203, 204, 158, 257]
read_lat = [60, 572, 236, 151, 65, 123]

lat_all = write_lat + read_lat
x_write_lat = x_groups[0] + offsets
x_read_lat = x_groups[1] + offsets
x_all_lat = np.concatenate([x_write_lat, x_read_lat])
bar_colors_lat = colors * 2

## ====================== 画图区域 ======================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.3))
plt.subplots_adjust(wspace=0.4, top=0.84, bottom=0.2)

## ===== (a) Throughput 柱状图 =====
def to_k(x, pos):
    return f'{x/1000:.0f}' if x % 1000 == 0 else f'{x/1000:.1f}'
ax1.yaxis.set_major_formatter(FuncFormatter(to_k))
ax1.set_yticks(np.arange(0, 16001, 4000))  ## 每隔 4k 一个刻度

ax1.set_ylabel("Throughput (GB/s)", fontsize=FONT_SIZE)
ax1.set_ylim(0, max(perf_all) * 1.2)
ax1.tick_params(axis='y', labelsize=FONT_SIZE)
for i, x in enumerate(x_all_perf):
    ax1.bar(x, perf_all[i], width=bar_width, color=bar_colors_perf[i], edgecolor='black')

ax1.set_xticks([])
ax1.set_xticks(x_groups, minor=True)
ax1.set_xticklabels(['Write', 'Read'], minor=True, fontsize=FONT_SIZE - 4)
ax1.tick_params(axis='x', which='minor')
ax1.set_xlabel("(a) Throughput", fontsize=FONT_SIZE)

## ===== (b) Latency 柱状图 =====
ax2.set_ylabel("Latency (μs)", fontsize=FONT_SIZE)
ax2.set_ylim(0, max(lat_all) * 1.2)
ax2.tick_params(axis='y', labelsize=FONT_SIZE)
ax2.set_yticks(np.arange(0, 601, 150))
for i, x in enumerate(x_all_lat):
    ax2.bar(x, lat_all[i], width=bar_width, color=bar_colors_lat[i], edgecolor='black')

ax2.set_xticks([])
ax2.set_xticks(x_groups, minor=True)
ax2.set_xticklabels(['Write', 'Read'], minor=True, fontsize=FONT_SIZE - 4)
ax2.tick_params(axis='x', which='minor')
ax2.set_xlabel("(b) Latency", fontsize=FONT_SIZE)

## ===== Legend (共用) =====
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors]
fig.legend(handles, devices, fontsize=FONT_SIZE - 8, loc='upper center',
           ncol=num_devices, bbox_to_anchor=(0.5, 0.98), columnspacing=1.22)

## 保存
plt.savefig("figs/btrfs_thpt_lat.pdf", bbox_inches='tight')
plt.show()

