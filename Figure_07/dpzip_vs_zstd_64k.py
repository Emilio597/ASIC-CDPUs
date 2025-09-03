import matplotlib.pyplot as plt
import numpy as np

chunksize = 4096*16

# Data for each algorithm
data = {
    "Algorithm": ["Snappy", "LZ4", "Deflate", "Zstd", "DPZip"],
    "Percentile Compressed File Size": [
        [8183,	12447,	16832,	24609,	30008,	31934,	33028,	35994,	40694,	51677,	65542],  # Snappy
        [8046,	12725,	17097,	25233,	30760,	32662,	33844,	35880,	40879,	50631,	64538],  # LZ4
        [6168,	9625,	11654,	17829,	22760,	24108,	25037,	29196,	30324,	41246,	61488], # Deflate
        [4221,	6551,	9301,	16618,	21534,	22723,	23734,	28291,	29699,	44599,	61981],  # Zstd
        [x * 16 for x in [506.47, 765.0, 896.0, 1263.0, 1675.0, 1780.0, 1881.0, 2087.0, 2636.0, 3156.0, 4113.0]],  # DPZip
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
plt.savefig("DPZip_Zstd_64k.pdf", format="pdf", bbox_inches="tight")
plt.show()

