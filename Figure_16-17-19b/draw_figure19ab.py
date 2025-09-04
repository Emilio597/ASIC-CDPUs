import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

FONT_SIZE = 18

## =================== 通用设置 ===================
devices = ["OFF", "Deflate(CPU)", "QAT 8970", "QAT 4XXX", "DP-CSD"]
colors = ['#BB433E','#E4C33F', '#A17C5B', '#81B181', '#429EBD']
num_devices = len(devices)

## =================== 子图：Btrfs ===================
write_throughput = [75.7, 11.75, 21.54, 25.20, 75.63]
read_throughput = [71.75, 23.41, 48.52, 52.33, 69.10]
write_cpu = [0.20, 29.15, 3.90, 3.21, 1.41]
read_cpu = [0.89, 14.12, 4.21, 4.46, 2.91]

# write_cpu = [i/100 * 176 for i in write_cpu]
# read_cpu = [i/100 * 176 for i in read_cpu]

bar_width = 0.20
group_gap = 0.1
x_groups = [0, 1 + group_gap]
offsets = (np.arange(num_devices) - (num_devices - 1)/2) * bar_width
x_write = x_groups[0] + offsets
x_read = x_groups[1] + offsets
x_all_btrfs = np.concatenate([x_write, x_read])
throughput_all = write_throughput + read_throughput
cpu_all_btrfs = write_cpu + read_cpu
bar_colors_btrfs = colors * 2

## =================== 子图：Microbench ===================
methods = ["QAT 8970", "QAT 4XXX", "DP-CSD", "Deflate(CPU)"]
# order_index = [1, 2, 3, 0]
order_index = [3, 0, 1, 2]

colors_micro = ['#A17C5B', '#81B181', '#429EBD', '#E4C33F']  # '#A17C5B', '#1A7EC1'
throughput_data = [
    [8.468856, 12.922635], [4.55, 9.31], [12.11, 13.75],
    [6.41, 16.66]
]
power_raw = [
    [840, 840], [804, 816], [828, 840],
    [912, 912]
]
power_raw = [[val - 755 for val in pair] for pair in power_raw]
power_eff = [
    [throughput_data[i][0] * 1024 / power_raw[i][0],
     throughput_data[i][1] * 1024 / power_raw[i][1]]
    for i in range(len(power_raw))
]
methods_ordered = [methods[i] for i in order_index]
values_ordered = [power_eff[i] for i in order_index]
colors_micro_ordered = [colors_micro[i] for i in order_index]

print(methods_ordered)
print(values_ordered)

micro_write_cpu = [3.17, 2.23, 0.6, 45.40]
micro_read_cpu = [3.17, 2.23, 0.6, 47.15]
cpu_all_micro = micro_write_cpu + micro_read_cpu


# write_cpu = [i/100 * 176 for i in write_cpu]
# read_cpu = [i/100 * 176 for i in read_cpu]



bar_width_micro = 0.20
bench_dc = ["Compress", "Decompress"]
base_x_micro = np.arange(len(bench_dc))

## =================== 创建两个子图 ===================
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(wspace=0.35, top=0.75, bottom=0.25)

## ========== (a) Microbench ========== #
ax1.set_ylabel("Pwr Eff. (MB/Joule)", fontsize=FONT_SIZE, labelpad=-3)
ax1.set_ylim(0, 250)
for i, (method, value) in enumerate(zip(methods_ordered, values_ordered)):
    offset = (i - (len(methods_ordered) - 1) / 2) * bar_width_micro
    x = base_x_micro + offset
    ax1.bar(x, value, width=bar_width_micro, color=colors_micro_ordered[i], edgecolor='k')
ax1.set_xticks(base_x_micro)
ax1.set_xticklabels(bench_dc, fontsize=FONT_SIZE)
ax1.tick_params(axis='y', labelsize=FONT_SIZE)
ax1.set_xlabel("(a) Microbench", fontsize=FONT_SIZE)

ax1r = ax1.twinx()
ax1r.set_ylabel("CPU Utilization", fontsize=FONT_SIZE)
ax1r.tick_params(axis='y', labelsize=FONT_SIZE, colors='red')
ax1r.set_ylim(0, max(cpu_all_micro) * 1.2)
ax1r.plot(x_write[:-1]+0.1, micro_write_cpu, 'o--', color='red')
ax1r.plot(x_read[:-1], micro_read_cpu, 'o--', color='red')

## ========== (b) Btrfs ========== #
ax3.set_ylabel("Pwr Eff. (MB/Joule)", fontsize=FONT_SIZE, labelpad=-3)
ax3.set_ylim(0, max(throughput_all) * 1.2)
for i, x in enumerate(x_all_btrfs):
    ax3.bar(x, throughput_all[i], width=bar_width, color=bar_colors_btrfs[i], edgecolor='black')
ax3.set_xticks([])
ax3.set_xticks(x_groups, minor=True)
ax3.set_xticklabels(['Write', 'Read'], minor=True, fontsize=FONT_SIZE)
ax3.tick_params(axis='x', which='minor')
ax3.tick_params(axis='y', labelsize=FONT_SIZE)
ax3.set_xlabel("(b) Btrfs", fontsize=FONT_SIZE)
ax3r = ax3.twinx()
ax3r.set_ylabel("CPU Utilization", fontsize=FONT_SIZE, )
ax3r.tick_params(axis='y', labelsize=FONT_SIZE, colors='red')
ax3r.set_ylim(0, max(cpu_all_btrfs) * 1.2)
ax3r.plot(x_write, write_cpu, 'o--', color='red')
ax3r.plot(x_read, read_cpu, 'o--', color='red')

## 图例
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i], edgecolor='black') for i in range(num_devices)]
fig.legend(handles, devices, fontsize=FONT_SIZE, loc='upper center',
           ncol=num_devices, bbox_to_anchor=(0.5, 0.90), columnspacing=.5, handletextpad=.5)

## 保存并显示
plt.subplots_adjust(wspace=0.55, top=0.75, bottom=0.25) 
plt.savefig("figs/power_eff.pdf", bbox_inches='tight', dpi=1200)
plt.show()
