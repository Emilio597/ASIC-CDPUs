import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import os

# -------- 创建输出目录 --------
os.makedirs("figs", exist_ok=True)

# -------- 图像参数 --------
FONT_SIZE = 20
# colors  = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#1A7EC1']
# markers = ['o', 's', '^', 'D', '*']
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#1A7EC1']
markers = ['o', '^', 's', 'D',  '*']
labels  = ["OFF","Deflate(CPU)","QAT8970", "QAT4XXX",  "DP-CSD"]

# -------- 图1数据：Latency vs Bandwidth --------
bandwidth = [
    400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000,
    4392, 4788, 5184, 5580, 5976, 6372, 6768, 7164, 7560, 7956, 8352, 8748
]
qat8970 = [8.6022, 8.55291, 8.60047, 8.55992, 8.52807, 8.5825, 8.55096, 8.54623,
           6.72171, 6.71308, 7.39453, 8.52, 25.56, 60.05, 69.78, 119.45, 174.54, 629.84,
           None, None, None, None]
qat4xxx = [8.28046, 8.82986, 8.7456, 8.8553, 8.03456, 8.44383, 8.21371, 8.75906,
           8.53817, 8.32044, 7.76231, 8.1, 19.36, 40.32, 134.6, 289.35, 343.55, 844.42,
           None, None, None, None]
cpu = [18.8112, 19.56443, 19.85466, 20.5, 92.73, 106.26, 138.73, 165.85,
       249.85, 348.66, None, None, None, None, None, None, None, None,
       None, None, None, None]
csd = [6.73105, 6.71983, 6.70795, 6.73078, 6.73057, 6.77365, 6.79873, 6.78123,
       6.30166, 6.75184, 6.72288, 6.74937, 6.32751, 6.42, 10.35, 30.18, 57.99,
       74.22, 326.3, 676.2, None, None]
nocomp = [5.24347, 5.85827, 5.60434, 5.75016, 5.64249, 5.59593, 5.61393, 5.60361,
          5.55254, 6.61158, 6.29994, 6.52138, 5.99769, 6.58129, 6.55, 12.48, 25.56,
          42.74, 69.43, 329.25, 545.5, 571.74]
lat_series = [nocomp, cpu, qat8970, qat4xxx, csd ]

# -------- 图2数据：P99.9 - P50 Latency --------
x_vals_all = [
        [4.55, 9.09, 13.64, 18.18, 22.73, 27.27, 31.82, 36.36, 40.91, 45.45,
     50.00, 54.54, 59.09, 63.63, 72.72, 77.27, 81.81, 86.36,
     90.90, 95.45, 100.00],
     [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    [5.55, 11.11, 16.67, 22.23, 27.79, 33.35, 38.91, 44.47, 50.03,
     55.59, 61.15, 66.71, 72.27, 77.83, 83.39, 88.95, 94.51, 100.00],
    [5.55, 11.11, 16.67, 22.23, 27.79, 33.35, 38.91, 44.47, 50.03,
     55.59, 61.15, 66.71, 72.27, 77.83, 83.39, 88.95, 94.51, 100.00],
    [5, 10, 15, 20, 25, 30, 35, 40, 45, 50,
     55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

]
y_vals_all = [
        [6672, 6128, 6640, 6384, 7248, 7984, 6000, 5552, 6192, 6320,
     6320, 6224, 6416, 8976, 876607376, 926938960,
     926938704, 935327312, 912752640, 201327000, 218104000],
         [11152, 11000, 11000, 54785328, 3305108432,
     3305106528, 3271552352, 3215408000, 3187408896, 3106930688],
    [9152, 9328, 9424, 9168, 9936, 9328, 8208, 9616, 8240,
     8464, 8816, 734000624, 1182791024, 1249899696, 1249899344,
     1233122704, 119567952, 432013312],
    [7920, 6768, 6704, 7440, 7472, 7536, 6832, 6960, 7152,
     7824, 7376, 39057072, 1115682320, 1149236496, 1193246000,
     1128137000, 1087636000, 322961408],

    [8528, 8400, 6064, 7216, 6768, 6448, 5392, 6416, 5808, 6224,
     6096, 6512, 10000, 76019408, 868218672, 968881904, 968881840,
     952104656, 962822144, 218104000]

]
x_vals_clean = [x for x in x_vals_all]
y_vals_clean = [[v / 1000 for v in y] for y in y_vals_all]  # ns → μs

# -------- 创建子图 --------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 图1: Latency vs Bandwidth
for i, y in enumerate(lat_series):
    x_plot = [bw for bw, v in zip(bandwidth, y) if v is not None]
    y_plot = [v for v in y if v is not None]
    ax1.plot(x_plot, y_plot, color=colors[i], marker=markers[i], linewidth=4, markersize=10)
ax1.set_xlabel("Bandwidth (MB/s)", fontsize=FONT_SIZE)
ax1.set_ylabel("Latency (ms)", fontsize=FONT_SIZE)
ax1.tick_params(axis='both', labelsize=FONT_SIZE)
ax1.grid(True, linestyle='--', alpha=.4)
ax1.text(0.5, -0.25, '(a) Latency vs Bandwidth', transform=ax1.transAxes,
         ha='center', fontsize=FONT_SIZE + 2)

# 图2: Tail Latency vs Percentile
for i in range(len(labels)):
    ax2.plot(x_vals_clean[i], y_vals_clean[i], color=colors[i], marker=markers[i], linewidth=4, markersize=10)
ax2.set_xlabel("Percentile (%)", fontsize=FONT_SIZE)
ax2.set_ylabel("P99.9 - P50 Latency (μs)", fontsize=FONT_SIZE)
ax2.set_yscale('log')
ax2.tick_params(axis='both', labelsize=FONT_SIZE)
ax2.grid(True, linestyle='--', alpha=.4)
ax2.text(0.5, -0.25, '(b) Tail Latency vs Percentile', transform=ax2.transAxes,
         ha='center', fontsize=FONT_SIZE + 2)

# -------- 图例 --------
legend_elems = [
    Line2D([0], [0], color=colors[i], marker=markers[i],
           linewidth=3, markersize=10, label=labels[i])
    for i in range(len(labels))
]
fig.legend(handles=legend_elems, loc='upper center',
           bbox_to_anchor=(0.5, 1.05),
           ncol=len(labels), fontsize=FONT_SIZE-4,
           handlelength=3, handletextpad=0.8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("figs/combined_latency_formatted.pdf", dpi=300, bbox_inches='tight')
plt.show()
