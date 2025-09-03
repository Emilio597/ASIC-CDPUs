import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

FONT_SIZE = 14
# 数据结构
data = {
    '4KB': {
        'level 1': [{'entropy': 1, 'LZ77': 7878, 'HUF': 6629, 'FSE': 3636},
                    {'entropy': 4, 'LZ77': 13453, 'HUF': 7170, 'FSE': 4597},
                    {'entropy': 7, 'LZ77': 11330, 'HUF': 7979, 'FSE': 3075}],
        'level 3': [{'entropy': 1, 'LZ77': 8213, 'HUF': 6425, 'FSE': 3588},
                    {'entropy': 4, 'LZ77': 13756, 'HUF': 6972, 'FSE': 3818},
                    {'entropy': 7, 'LZ77': 14169, 'HUF': 7187, 'FSE': 3173}],
        'level 10': [{'entropy': 1, 'LZ77': 74281, 'HUF': 5964, 'FSE': 4373},
                     {'entropy': 4, 'LZ77': 176575, 'HUF': 6346, 'FSE': 5205},
                     {'entropy': 7, 'LZ77': 74881, 'HUF': 7261, 'FSE': 4497}],
    },
    '16KB': {
        'level 1': [{'entropy': 1, 'LZ77': 13036, 'HUF': 6399, 'FSE': 6528},
                    {'entropy': 4, 'LZ77': 35059, 'HUF': 9531, 'FSE': 9784},
                    {'entropy': 7, 'LZ77': 30715, 'HUF': 15540, 'FSE': 5677}],
        'level 3': [{'entropy': 1, 'LZ77': 14263, 'HUF': 6380, 'FSE': 6661},
                    {'entropy': 4, 'LZ77': 36865, 'HUF': 8560, 'FSE': 8345},
                    {'entropy': 7, 'LZ77': 53266, 'HUF': 13855, 'FSE': 6612}],
        'level 10': [{'entropy': 1, 'LZ77': 174271, 'HUF': 5824, 'FSE': 7761},
                     {'entropy': 4, 'LZ77': 906327, 'HUF': 7298, 'FSE': 8986},
                     {'entropy': 7, 'LZ77': 318555, 'HUF': 13068, 'FSE': 7338}],
    },
    '128KB': {
        'level 1': [{'entropy': 1, 'LZ77': 62804, 'HUF': 12904, 'FSE': 12756},
                    {'entropy': 4, 'LZ77': 269228, 'HUF': 37730, 'FSE': 29767},
                    {'entropy': 7, 'LZ77': 204876, 'HUF': 94706, 'FSE': 16221}],
        'level 3': [{'entropy': 1, 'LZ77': 71072, 'HUF': 12335, 'FSE': 12292},
                    {'entropy': 4, 'LZ77': 325288, 'HUF': 35627, 'FSE': 28319},
                    {'entropy': 7, 'LZ77': 349110, 'HUF': 93315, 'FSE': 16182}],
        'level 10': [{'entropy': 1, 'LZ77': 756386, 'HUF': 12241, 'FSE': 15226},
                     {'entropy': 4, 'LZ77': 3158982, 'HUF': 28090, 'FSE': 30674},
                     {'entropy': 7, 'LZ77': 1947728, 'HUF': 41014, 'FSE': 26846}],
    },
}

compression_ratios = {
    'level 1': {'4KB': [14.36, 42.26, 88.06], '16KB': [11.15, 40.41, 86.99], '128KB': [9.95, 47.61, 87.01]},
    'level 3': {'4KB': [15.75, 41.70, 82.18], '16KB': [10.99, 38.18, 86.63], '128KB': [9.84, 46.77, 87.02]},
    'level 10': {'4KB': [14.40, 35.50, 82.20], '16KB': [10.61, 32.65, 85.25], '128KB': [9.47, 44.01, 84.44]},
}

fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), sharey=True)
algorithms = ['LZ77', 'HUF', 'FSE']
colors = {'LZ77': '#89C7CB', 'HUF': '#F4F4B4', 'FSE': '#FDAE86'}
patterns = {1: 'o', 4: '', 7: '..'}
entropy_values = [1, 4, 7]
levels = ['level 1', 'level 3', 'level 10']
file_sizes = ['4KB', '16KB', '128KB']
width = 0.25

for idx, (ax, size) in enumerate(zip(axes, file_sizes)):
    indices = np.arange(len(levels))
    for k, entropy in enumerate(entropy_values):
        for i, level in enumerate(levels):
            lz77 = data[size][level][k]['LZ77']
            huf = data[size][level][k]['HUF']
            fse = data[size][level][k]['FSE']
            total = lz77 + huf + fse
            base_x = i + (k - 1) * width
            ax.bar(base_x, lz77 / total * 100, width=width,
                   color=colors['LZ77'], hatch=patterns[entropy], edgecolor='black')
            ax.bar(base_x, huf / total * 100, width=width,
                   bottom=lz77 / total * 100,
                   color=colors['HUF'], hatch=patterns[entropy], edgecolor='black')
            ax.bar(base_x, fse / total * 100, width=width,
                   bottom=(lz77 + huf) / total * 100,
                   color=colors['FSE'], hatch=patterns[entropy], edgecolor='black')

    ax2 = ax.twinx()
    for i, level in enumerate(levels):
        x = [i + (k - 1) * width for k in range(3)]
        y = compression_ratios[level][size]
        ax2.plot(x, y, marker='o', color='orangered', linewidth=1)

    ax.set_xticks(indices)
    ax.set_xticklabels(levels, fontsize=FONT_SIZE)
    ax.tick_params(axis='y', labelsize=FONT_SIZE)
    ax.set_ylim(0, 100)
    if idx == 0:
        ax.set_ylabel('Compression Time (%)', fontsize=FONT_SIZE)
        ax.yaxis.set_tick_params(
            labelleft=True, 
            left=True,
            labelsize=FONT_SIZE,
            labelcolor='black'
        )
    else:
        ax.yaxis.set_tick_params(
            labelleft=False, 
            left=False
        )

    ax2.set_ylim(0, 100)
    if idx == 2:
        ax2.set_ylabel('Compression Ratio', fontsize=FONT_SIZE, color='red')
        ax2.tick_params(axis='y', colors='red',labelsize =FONT_SIZE) # 设置刻度颜色为红色
    else:
        ax2.set_yticklabels([])

    #ax.set_title(size, fontsize=11)
    ax.text(0.5, -0.17, f'{size}', transform=ax.transAxes,
        ha='center', va='center', fontsize=FONT_SIZE)

# 图例
handles_color = [mpatches.Patch(color=colors[alg], label=alg) for alg in algorithms]
handles_pattern = [mpatches.Patch(facecolor='white', edgecolor='black', hatch=patterns[ent], label=f'Entropy {ent}') for ent in patterns]

fig.legend(handles=handles_color + handles_pattern,
           ncol=6, loc='upper center', bbox_to_anchor=(0.495, 1.08), fontsize=FONT_SIZE - 3)

fig.tight_layout()
plt.subplots_adjust(bottom=0.23, wspace=0.15)
#plt.show()
plt.savefig('ZSTDbreakdown2.pdf', bbox_inches="tight", pad_inches=0, dpi=1200)
plt.show()

