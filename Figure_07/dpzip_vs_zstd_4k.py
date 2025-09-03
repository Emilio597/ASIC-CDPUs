import matplotlib.pyplot as plt
import numpy as np

chunksize = 4096

# Data for each algorithm
data = {
    "Algorithm": ["Snappy", "LZ4", "Deflate", "Zstd", "DPZip"],
    "Percentile Compressed File Size": [
        [722, 1077, 1277, 1731, 2234, 2401, 2548, 2862, 3133, 3830, 4101],  # Snappy
        [768, 1117, 1307, 1817, 2316, 2501, 2628, 2840, 3170, 3675, 4119],  # LZ4
        [501, 755, 880, 1233, 1637, 1749, 1849, 2075, 2402, 3028, 4119], # Deflate
        [376, 629, 734, 1188, 1619, 1729, 1827, 2042, 2535, 3146, 4106],  # Zstd
        [506.47, 765.0, 896.0, 1263.0, 1675.0, 1780.0, 1881.0, 2087.0, 2636.0, 3156.0, 4113.0],  # DPZip
    ],
    "Percentiles": [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99],
}

# Plotting the graph
plt.figure(figsize=(3.5, 3.2))

# Define colors for each algorithm
colors = ['b', 'g', 'c', 'm', 'r']

# Define markers for each algorithm
markers = ['o', 's', '^', 'D', '*']

# Plot the percentiles for each algorithm
for idx, algorithm in enumerate(data["Algorithm"]):
    plt.plot(data["Percentiles"],  [x / chunksize for x in data["Percentile Compressed File Size"][idx]], label=algorithm, marker=markers[idx], color=colors[idx])

# Adding labels and title
plt.xlabel('Percentile (%)')
plt.ylabel('Compression ratio')
#plt.title('Percentile Distribution of Compressed File Sizes')
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.savefig("DPZip_Zstd_4k.pdf", format="pdf", bbox_inches="tight")
plt.show()

