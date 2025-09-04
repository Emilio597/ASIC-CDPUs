import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

FONT_SIZE = 24

## 设置方法、颜色、标签
bench_dc = ["Compress", "Decompress"]
#colors = ['#DD514C', '#F37B1D', '#FAD232', '#5EB95E', '#1F8DD6', '#8058A5']
#dark version
colors = ['#BB433E', '#D36C1D', '#E4C33F', '#81B181', '#A17C5B', '#1A7EC1']
methods = ["QAT 8970", "QAT 4XXX", "DPZip", "Deflate(CPU)", "ZSTD(CPU)", "Snappy(CPU)"]
order_index = [5, 3, 4, 0, 1, 2]

## 原始数据（只保留吞吐量和时延）
data = {
    "Throughput64KB": [
        [8.47, 12.92], [4.55, 9.31], [12.11, 13.75],
        [6.41, 16.66], [20.35, 22.26], [23.15, 23.06]
    ],
    "Latency": [
        [172.0, 63.0], [34, 21.0], [11.50, 3.35],
        [832.28, 272.91], [213, 66], [172.17, 67.16]
    ]
}

## 配置
y_labels = {
    "Throughput64KB": "Throughput (GB/s)",
    "Latency": "Latency (μs)"
}
x_labels = {
    "Throughput64KB": "(a) Throughput",
    "Latency": "(b) Latency"
}
y_lims = {
    "Throughput64KB": (0, 55),
    "Latency": (0, 75)
}

## 创建子图
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(wspace=0.28, bottom=0.2, left=0.08, right=0.99, top=0.80)
bar_width = 0.11
num_methods = len(methods)

## 绘图主循环
for ax, (metric, values) in zip(axes, data.items()):
    methods_ordered = [methods[i] for i in order_index]
    values_ordered = [values[i] for i in order_index]

    base_x = np.arange(len(bench_dc))
    for i, (method, value) in enumerate(zip(methods_ordered, values_ordered)):
        offset = (i - (num_methods - 1) / 2) * bar_width
        x = base_x + offset
        bars = ax.bar(x, value, width=bar_width, color=colors[i], edgecolor='k')

        if method in ["QAT 4XXX", "DPZip"]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                        f"{height:.1f}", ha='center', va='bottom', fontsize=FONT_SIZE - 4,rotation=90)

    ax.set_xticks(base_x)
    ax.set_xticklabels(bench_dc, fontsize=FONT_SIZE)
    ax.set_ylabel(y_labels[metric], fontsize=FONT_SIZE)
    ax.set_xlabel(x_labels[metric], fontsize=FONT_SIZE)
    #ax.set_ylim(*y_lims[metric])
    if metric == "Latency":
        max_val = max(max(v) for v in values_ordered)
        ax.set_ylim(0, max_val * 1.2)  ## 留出 20% 空间
    else:
        ax.set_ylim(*y_lims[metric])
    ax.tick_params(axis='y', labelsize=FONT_SIZE)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))

    if metric == "Throughput64KB":
        ax.set_ylim(0, 32)
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

## 保存
plt.savefig('figs/microbench_64kb_thpt_lat.pdf', pad_inches=0, format='pdf', dpi=1200)
plt.show()

