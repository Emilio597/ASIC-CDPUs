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
1. **Software-Only Environment (CPU-based):** Used for algorithm analysis, compression ratio comparisons, and some microbenchmarks. This relies on standard CPU execution without specialized hardware.
   - **OS:** Ubuntu 20.04 or later (tested on Linux kernel 5.15+).
   - **CPU:** Intel Xeon (e.g., 88 threads as in the paper), but scalable to multi-core systems.
   - **Dependencies:**
     - Python 3.8+ with libraries: `numpy`, `matplotlib`, `pandas` (install via `pip install numpy matplotlib pandas`).
     - C/C++ compiler (e.g., GCC 9+ for building Zstd or other tools).
     - Compression libraries: Zstd (v1.5.2+), Deflate (via zlib), LZ4, Snappy (install via apt: `sudo apt install libzstd-dev zlib1g-dev liblz4-dev libsnappy-dev`).
     - Tools: `make`, `cmake` (for building in `Figure_02`).
   - **Setup Script:** Run `conda create -n soft-env python=3.8` (if using Conda) or use a virtualenv, then install dependencies.

2. **Hardware-Accelerated Environment:** Used for throughput, latency, and power tests involving accelerators like QAT 8970, QAT 4xxx, DPZip, and DP-CSD. This requires specific hardware and drivers.
   - **Hardware:** 
     - Intel QAT 8970 (PCIe card) or QAT 4xxx (on-chip).
     - DP-CSD (custom ASIC-based in-storage accelerator; assumes access to prototype hardware).
     - SSDs (e.g., for 4KB/64KB block tests) and NAND flash for DP-CSD.
     - Multi-socket system for scaling (e.g., 2-socket Intel Xeon for QAT 4xxx).
   - **OS and Drivers:** Ubuntu 20.04+ with Intel QAT drivers (e.g., QATlib for user-space acceleration). Firmware files are included in `Figure_16-18b/btrfs_qat_firmware`.
     - Install QAT: Download from Intel (e.g., QuickAssist Technology Driver), build and load modules (`modprobe qat_api`).
     - For DP-CSD: Custom firmware and drivers (not included; contact authors for details).
   - **Dependencies:** Same as software environment, plus:
     - `fio` for I/O benchmarking (`sudo apt install fio`).
     - `iostat`, `perf` for monitoring.
     - RocksDB, Btrfs, ZFS for application tests (install via apt or build from source).
   - **Setup Notes:** Bind processes to NUMA nodes for optimal performance (e.g., via `numactl`). Power measurements require tools like Intel PCM or a power meter.

Figures using **Software-Only Environment**: Figure 2, 7, 11, 12 (primarily analysis and plotting).
Figures using **Hardware-Accelerated Environment**: Figure 8, 9, 14, 15, 16, 18, 19, 20 (involve QAT, DP-CSD, or storage systems).

**General Tips:**
- Activate the environment: `conda activate soft-env` or similar.
- Data Generation: Use tools like `datagen` in Zstd for synthetic data with varying entropy.
- Workloads: YCSB for RocksDB (requires building RocksDB with compression enabled).

## Usage and Testing Methods

To reproduce a figure:
1. Navigate to the corresponding folder.
2. Set up the required environment (as noted below).
3. Run the test/execution script(s) to generate data.
4. Run the drawing script (e.g., Python plotter) to visualize.

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
- **Description:** Summarizes compression/decompression throughput for Deflate, QAT 8970, QAT 4xxx, DPZip (e.g., 5.6GB/s compression for DPZip).
- **Environment:** Hardware-Accelerated.
- **Steps:**
  1. `cd Figure_08-09-19a/lzbench_test`.
  2. Run `./run_lzbench.sh` (or `./run_lzbench_numa.sh` for NUMA-binding) to benchmark.
  3. For peak tests: `cd ../peak_test`, run subfolder scripts (e.g., for QAT 8970/4xxx).
  4. Plot: Use `python bw.py` on output logs (e.g., `output_lzbench.log`).

### Figure 9: Throughput at 64KB Granularity
- **Description:** Shows throughput gains with larger I/O (30–177% improvements), including multi-DP-CSD scaling.
- **Environment:** Hardware-Accelerated.
- **Steps:** Similar to Figure 8; uses same `lzbench_test` folder. Focus on 64KB configs in `run_lzbench.sh`.

### Figure 11: QAT Latency Breakdown
- **Description:** Illustrates processing flow and latency (e.g., 448ns for QAT 4xxx on 64KB).
- **Environment:** Software-Only (post-processing).
- **Steps:** Run `python draw.py` (assumes telemetry data from hardware tests; collect via QAT tools).

### Figure 12: Performance Robustness
- **Description:** DPZip vs. QAT robustness across compressibility (e.g., <15% drop for DPZip).
- **Environment:** Software-Only (plotting).
- **Steps:** Run `python draw.py` (uses data from throughput tests).

### Figure 14: YCSB Throughput (RocksDB Workloads A & F)
- **Description:** End-to-end OPS under scaling concurrency for QAT, CPU, DP-CSD.
- **Environment:** Hardware-Accelerated (requires RocksDB build).
- **Steps:**
  1. `cd Figure_14-15-20`.
  2. Run`./run_all.sh` for workloads.
  3. Analyze: `cd analyze_thrpt`, run `python batch_collect.py` and `python cal_thrpt.py`.
  4. Plot throughput: draw_xxx.py

### Figure 15: YCSB Read Latency (RocksDB Workloads A & F)
- **Description:** Average latency across configurations.
- **Environment:** Hardware-Accelerated.
- **Steps:** Similar to Figure 14; use `./run_lat_test.sh` and `cal_ycsb/cal_avg_lat.py`.

### Figure 16: Btrfs Throughput and Latency
- **Description:** Throughput/loss in async compression; latency with read amplification (e.g., 5μs overhead for DP-CSD).
- **Environment:** Hardware-Accelerated (Btrfs setup).
- **Steps:**
  1. `cd Figure_16-17-19b/version_CDF`.
  2. Set env: `./set_variables_new.sh`.
  3. Run `./run_throughput_test_CDF.sh` with FIO configs.
  4. Stats: `./stat_cpuutil_power.sh`.

### Figure 16: Btrfs Throughput and Latency
- **Description:** Throughput/loss in async compression; latency with read amplification (e.g., 5μs overhead for DP-CSD).
- **Environment:** Hardware-Accelerated (Btrfs setup).
- **Steps:**
  same as Figure 16

### Figure 18: ZFS Latency Across Record Sizes
- **Description:** Latency for CPU, QAT, etc., across 4KB–128KB (higher for CPU).
- **Environment:** Hardware-Accelerated (ZFS setup).
- **Steps:**
  1. `cd Figure_18`.
  2. Run `./run_throughput_test.sh` with FIO files.
  3. Get ratios: `./get_compress_ratio.sh`.

### Figure 19: Power Efficiency (Microbenchmarks and Btrfs)
- **Description:** MB/J for DPZip (169–395) vs. others; CPU utilization.
- **Environment:** Hardware-Accelerated.
- **Steps:** Use data from Figure_08-09-19a and Figure 16-17-19b; run power scripts like `collect_thrpt_and_power_verbose.py`.

### Figure 20: Power Efficiency in RocksDB (YCSB)
- **Description:** OPS/J for DPZip (up to 5224) vs. QAT/CPU.
- **Environment:** Hardware-Accelerated.
- **Steps:** Similar to Figure Figure_14-15-20 aggregate in `stats_aggr_workloada/print_each_task_power.py`.

## Contributing and License
Contributions welcome for improvements or ports to new hardware. Licensed under MIT; see individual folders for third-party code (e.g., Zstd under BSD).

For issues, contact the authors. Results reproduction requires matching hardware; software-only figures are easier to replicate.
