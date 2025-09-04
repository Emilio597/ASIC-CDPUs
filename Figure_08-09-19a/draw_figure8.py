import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

FONT_SIZE = 24

## 方法顺序 & 颜色
methods = ["QAT 8970", "QAT 4XXX", "DPZip", "Deflate(CPU)", "ZSTD(CPU)", "Snappy(CPU)"]
order_index = [5, 3, 4, 0, 1, 2]
#colors = ['#DD514C', '#F37B1D', '#FAD232', '#5EB95E', '#1F8DD6', '#8058A5']
#dark version
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#A17C5B', '#1A7EC1']
## 原始数据（仅保留需要的两个）
data = {
    "Throughput4KB": [
        [4.86, 7.20], [2.06, 3.45], [5.6, 9.38],
        [4.90, 13.57], [15.55, 19.13], [22.83, 20.33]
    ],
    "Latency": [
        [27.0, 14.0], [9.0, 6.0], [4.67, 2.15],
        [69.58, 23.69], [20.37, 7.44], [8.87, 3.75]
    ]
}

## 图配置
y_labels = {
    "Throughput4KB": "Throughput (GB/s)",
    "Latency": "Latency (μs)",
}
x_labels = {
    "Throughput4KB": "(a) Throughput",
    "Latency": "(b) Latency",
}
y_lims = {
    "Throughput4KB": (0, 55),
    "Latency": (0, 75)
}
label_size = {"Throughput4KB": 9, "Latency": 9}

## 子图设置：只创建两个子图
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(wspace=0.28, bottom=0.2, left=0.08, right=0.99 ,top=0.80)
bar_width = 0.11
num_methods = len(methods)
bench_dc = ["Compress", "Decompress"]

for ax, (metric, values) in zip(axes, data.items()):
    methods_ordered = [methods[i] for i in order_index]
    values_ordered = [values[i] for i in order_index]

    x_labels_this = bench_dc
    cur_width = bar_width
    base_x = np.arange(len(x_labels_this))
    for i, (method, value) in enumerate(zip(methods_ordered, values_ordered)):
        offset = (i - (num_methods - 1) / 2) * cur_width
        x = base_x + offset
        bars = ax.bar(x, value, width=cur_width, color=colors[i], edgecolor='k')
        
        if method in ["QAT 4XXX", "DPZip"]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                        f"{height:.1f}", ha='center', va='bottom', fontsize=FONT_SIZE - 4,rotation=90)
    ax.set_xticks(base_x)
    ax.set_xticklabels(x_labels_this, fontsize=FONT_SIZE)

    ax.set_ylabel(y_labels[metric], fontsize=FONT_SIZE)
    ax.set_xlabel(x_labels[metric], fontsize=FONT_SIZE)
    ax.set_ylim(*y_lims[metric])
    ax.tick_params(axis='y', labelsize=FONT_SIZE)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))

    if metric == "Throughput4KB":
        ax.set_ylim(0, 32)  ## 设置纵坐标范围为 0~30
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=3))
    else:
        ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    

## 图例放置在顶部，两排
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i], edgecolor='k') for i in range(num_methods)]
fig.legend(
    handles, methods_ordered,
    loc='upper center',
    bbox_to_anchor=(0.535, 1.0),  ## 提高位置为两排腾出空间
    ncol=3,                        ## 每行显示3个，共两行
    fontsize=FONT_SIZE - 8,      ## 可调整字号以避免重叠
    columnspacing=6.0,
    handletextpad=1.0
)


## 保存图
plt.savefig('figs/microbench_4kb_thpt_lat.pdf', pad_inches=0, format='pdf', dpi=1200)
plt.show()

