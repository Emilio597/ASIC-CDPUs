# ASIC-based Compression Accelerators for Storage Systems: Code and Scripts for Paper Figures

## Project Overview

This repository contains the open-source test code, scripts, and supporting files used to generate the experimental results and figures in the paper titled "ASIC-based Compression Accelerators for Storage Systems: Design, Placement, and Profiling Insights." The paper explores modern compression algorithms (e.g., Zstd, Deflate, LZ4, Snappy) and hardware accelerators (e.g., DPZip, QAT 8970, QAT 4xxx, DP-CSD) in storage systems, focusing on metrics like compression ratio, throughput, latency, power efficiency, and robustness across varying parameters such as block sizes (4KB–128KB), compression levels, and data entropy.

Key findings from the paper include:
- LZ77 operations dominate computational costs in algorithms like Zstd, especially at higher compression levels.
- DPZip matches or outperforms traditional compressors in ratio and throughput, with superior robustness on incompressible data.
- Larger I/O granularities (e.g., 64KB) boost throughput but may increase read amplification.
- Hardware placement (e.g., in-storage vs. on-chip) impacts latency and efficiency.
- DP-CSD achieves the highest power efficiency across device, system, and application levels (e.g., up to 5224 OPS/J in RocksDB workloads).

The code is organized into folders named after the corresponding figures (e.g., `Figure_02`, `Figure_07`). Each folder includes scripts for running tests, processing data, and generating plots. This allows reproduction of the experiments on similar hardware setups.

**Note:** Results may vary based on exact hardware, software versions, and workloads. The code assumes access to specific accelerators (e.g., Intel QAT, DP-CSD) for hardware-related tests.

## Environment Setup

The experiments use two primary environments due to the mix of software-only and hardware-accelerated tests:

1. **Software-Only Environment (CPU-based):**
   Used for algorithm analysis, compression ratio comparisons, and some microbenchmarks.

   * **OS:** Ubuntu 20.04 or later (tested on Linux kernel 5.15, 6.5, 6.9).
   * **CPU:** Intel Xeon 8458P.
   * **Dependencies:**

     * Python 3.8+ with `numpy`, `matplotlib`, `pandas` (`pip install numpy matplotlib pandas`).
     * C/C++ compiler (e.g., GCC 9+).
     * Compression libraries: Zstd (v1.5.2+), zlib, LZ4, Snappy.
     * Tools: `make`, `cmake`.

2. **Hardware-Accelerated Environment:**
   Used for throughput, latency, and power tests involving accelerators like QAT 8970, QAT 4xxx, DPZip, and DP-CSD.

   * **Hardware:** Intel QAT 8970 (PCIe card), QAT 4xxx (on-chip), DP-CSD, SSDs/NAND.
   * **Dependencies:** Same as above, plus `fio`, `iostat`, `perf`, RocksDB, Btrfs, ZFS.
   * **Drivers:** Intel QAT drivers (QATlib) and custom drivers for DP-CSD.

### Kernel Requirements

Different experiments require different Linux kernels:

* **Linux 6.9.0 (with patch):**
  Required for Btrfs experiments in **Figure 16, Figure 17, and Figure 19b**.

  * Patch file: `Figure_16-17-19b/linux6.9.0.patch`.
  * Apply patch to vanilla 6.9.0 source and build a custom kernel manually.

* **Linux 5.15:**
  Used for QAT 8970 experiments in **Figure 8, Figure 9, and Figure 19a**.

* **Linux 6.5:**
  Default kernel for most other experiments, including SSD tests, QAT 4xxx experiments, and all other figures not explicitly listed above.

Figures using **Software-Only Environment**: Figure 2, 7, 11, 12 (primarily analysis and plotting).
Figures using **Hardware-Accelerated Environment**: Figure 8, 9, 14, 15, 16, 18, 19, 20 (involve QAT, DP-CSD, or storage systems).

**General Tips:**
- Activate the environment: `conda activate soft-env` or similar.
- Data Generation: Use tools like `datagen` in Zstd for synthetic data with varying entropy.
- Workloads: YCSB for RocksDB (requires building RocksDB with compression enabled).

## Usage and Testing Methods

To reproduce a figure:
1. Navigate to the corresponding folder.
2. Ensure the correct kernel version (see **Kernel Requirements**).
3. Run the provided test/execution script(s) to generate data.
4. Use the drawing script (Python) to plot results.

Detailed instructions per figure:

### Figure 2: Zstd Algorithm Analysis
- **Description:** Analyzes LZ77 dominance, entropy coding impact, and parameter effects (chunk size, compression level, entropy).
- **Environment:** Software-Only.
- **Steps:**
  1. Build Zstd: `cd Figure_02/build/cmake && cmake . && make`.
  2. Run tests: `./test.sh` (executes benchmarks on modified Zstd code).
  3. Generate plot: `python draw.py` (uses data from tests to plot computational costs).

### Figure 7: Compression Ratio Comparison
- **Description:** Compares ratios across algorithms (DPZip, Deflate, Zstd, Snappy, LZ4) at 4KB and 64KB blocks.
- **Environment:** Software-Only.
- **Steps:**
  1. Run `python dpzip_vs_zstd_4k.py` for 4KB results.
  2. Run `python dpzip_vs_zstd_64k.py` for 64KB results (plots percentiles automatically).

### Figure 8: Throughput at 4KB Granularity
- **Description:** Compares compression/decompression throughput across hardware accelerators and CPU-based algorithms at 4KB block granularity.
- **Environment:** Hardware-Accelerated.
- **Steps:**
  1. `cd Figure_08-09-19a/lzbench_test`.
  2. Run `./run_lzbench.sh` or `./run_lzbench_numa.sh` for NUMA-binding tests.
  3. For peak tests: `cd ../peak_test`, run scripts in `qat_8970/`, `qat_4xxx/` subfolders.
  4. Generate plot: `python draw_figure8.py`.

### Figure 9: Throughput at 64KB Granularity
- **Description:** Shows throughput improvements with larger I/O granularity (64KB) across different compression methods.
- **Environment:** Hardware-Accelerated.
- **Steps:**
  1. `cd Figure_08-09-19a/lzbench_test`.
  2. Run `./run_lzbench.sh` or `./run_lzbench_numa.sh` (configured for 64KB blocks).
  3. For peak tests: `cd ../peak_test`, test accelerators in respective subfolders.
  4. Generate plot: `python draw_figure9.py`.

### Figure 11: QAT Latency Breakdown
- **Description:** Illustrates processing flow and latency (e.g., 448ns for QAT 4xxx on 64KB).
- **Environment:** Software-Only (post-processing).
- **Steps:** Run `python draw.py` (assumes telemetry data from hardware tests; collect via QAT tools).

### Figure 12: Performance Robustness
- **Description:** DPZip vs. QAT robustness across compressibility (e.g., <15% drop for DPZip).
- **Environment:** Software-Only (plotting).
- **Steps:** Run `python draw.py` (uses data from throughput tests).

### Figure 14: YCSB Throughput (RocksDB Workloads A & F)
- **Description:** Measures end-to-end OPS under scaling concurrency for QAT, CPU, and DP-CSD.
- **Environment:** Hardware-Accelerated (requires RocksDB build).
- **Steps:**
  1. `cd Figure_14-15-20`.
  2. Run `./run_all.sh` for workloads.
  3. Analyze results: `cd analyze_thrpt`, run `python batch_collect.py` and `python cal_thrpt.py`.
  4. Generate plot: `python draw_figure14.py`.


### Figure 15: YCSB Read Latency (RocksDB Workloads A & F)
- **Description:** Evaluates average latency across different configurations.
- **Environment:** Hardware-Accelerated.
- **Steps:**
  1. `cd Figure_14-15-20`.
  2. Run `./run_lat_test.sh`.
  3. Calculate average latency: `python cal_ycsb/cal_avg_lat.py`.
  4. Generate plot: `python draw_figure15.py`.

### Figure 16, 17: Btrfs Throughput and Latency

* **Description:** Evaluates throughput and latency in asynchronous compression with read amplification.
* **Kernel Requirement:** Must use Linux 6.9.0 **with patch** (`Figure_16-17-19b/linux6.9.0.patch`). Compile and install manually before testing.
* **Steps:**

  1. Apply patch to Linux 6.9.0, compile, reboot into patched kernel.
  2. `cd Figure_16-17-19b/version_CDF`.
  3. Set environment variables: `./set_variables_new.sh`.
  4. Run throughput tests: `./run_throughput_test_CDF.sh`.
  5. Collect statistics: `./stat_cpuutil_power.sh`.

### Figure 18: ZFS Latency Across Record Sizes
- **Description:** Measures latency for CPU, QAT, and other configurations across various record sizes.
- **Environment:** Hardware-Accelerated (ZFS setup).
- **Steps:**
  1. `cd Figure_18/zfs_qat_test`.
  2. Run tests: `./run_test.sh`.
  3. Calculate compression ratios: `./comp_ratio_test.sh`.

### Figure 19: Power Efficiency (Microbenchmarks and Btrfs)
- **Description:** Analyzes power efficiency (MB/J) for DPZip compared to other methods.
- **Environment:** Hardware-Accelerated.
- **Steps:**
  1. Use data from `Figure_08-09-19a` and `Figure_16-17-19b`.
  2. Run power scripts: `collect_thrpt_and_power_verbose.py`.
  3. Generate plot: `python draw_figure19ab.py` (in Figure_16-17-19b).

### Figure 20: Power Efficiency in RocksDB (YCSB)
- **Description:** Analyzes OPS/J for DPZip compared to QAT and CPU.
- **Environment:** Hardware-Accelerated.
- **Steps:**
  1. `cd Figure_14-15-20`.
  2. Aggregate results: `python stats_aggr_workloada/print_each_task_power.py`.
  3. Generate plot: `python draw_figure20.py`.

## Contributing and License
Contributions welcome for improvements or ports to new hardware. Licensed under MIT; see individual folders for third-party code (e.g., Zstd under BSD).

For issues, contact the authors. Results reproduction requires matching hardware; software-only figures are easier to replicate.
