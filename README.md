# ASIC-based Compression Accelerators for Storage Systems — Artifact (EuroSys’26)

**Artifact type:** Code + scripts + data generators to reproduce paper figures  
**Target badges:** _Artifacts Available_, _Artifacts Functional_, _Results Reproduced (subset/full, depending on hardware)_

## 0) What this artifact demonstrates (claims we validate)

- **C1. Cost dominance.** LZ77-family stages dominate CPU-side cost in Zstd-like compressors; effect increases with compression level.  
- **C2. Robustness.** DPZip is competitive or better on ratio/throughput and drops less on near-incompressible data.  
- **C3. Granularity.** Larger I/O granularities (e.g., 64 KB) increase throughput but may elevate read amplification.  
- **C4. Placement.** Accelerator placement (in-storage vs. host/on-chip) materially impacts performance and energy.

Each figure folder contains scripts to regenerate the corresponding results. CPU-only figures reproduce on any recent x86_64 Linux; hardware figures require the listed accelerators.

---

## 1) Repository layout (high-level)

```
Figure_02/                  # Zstd algorithm analysis (CPU-only)
Figure_07/                  # Compression ratio comparison (CPU-only)
Figure_08-09-19a/           # 4KB / 64KB throughput; power (QAT 8970 focus)
Figure_11/                  # QAT latency breakdown (post-processing)
Figure_12/                  # Robustness across compressibility (plotting)
Figure_14-15-20/            # RocksDB+YCSB end-to-end throughput, latency, OPS/J
Figure_16-17-19b/           # Btrfs async compression: thr/lat + power (Linux 6.9.0 + patch)
Figure_18/                  # ZFS latency vs. record size (QAT/CPU)
```

> Each figure folder has: `README.md` (short), `run_*.sh` or `*.py` (driver), `draw_*.py` (plot), and output directory hints.

---

## 2) Quick start (pick one path)

### Path A — **CPU-only (fastest smoke test)**
Reproduces Figures **2, 7, 11, 12** plots from locally generated or provided data.

```bash
# Python env (conda or venv)
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip numpy pandas matplotlib

# Figure 02
cd Figure_02 && cd zstd/build/cmake && cmake . && make && ../../test.sh
python draw.py                         # regenerates Figure 2

# Figure 07
cd ../Figure_07
python dpzip_vs_zstd_4k.py
python dpzip_vs_zstd_64k.py
```

### Path B — **Full hardware (QAT / DPZip / DP-CSD)**
Requires drivers, kernel setup, and boards present. See **Environment & Kernel** and per-figure sections below.

---

## 3) Environment & dependencies

### 3.1 Software-only environment
- **OS:** Ubuntu 20.04+ (tested with Linux **5.15**, **6.5**, **6.9**).  
- **CPU:** x86_64 (tested on Intel Xeon 8458P).  
- **Tooling:** `gcc` (9+), `cmake`, `make`, Python 3.8+ (`numpy`, `pandas`, `matplotlib`).  
- **Compression libs:** Zstd (≥1.5.2), zlib, LZ4, Snappy.

### 3.2 Hardware-accelerated environment
- **Accelerators (any subset):** Intel **QAT 8970** (PCIe), **QAT 4xxx** (on-chip), **DPZip**, **DP-CSD**.  
- **Storage stacks:** SSD(s)/NAND, RocksDB (built w/ compression), Btrfs, ZFS.  
- **Tools:** `fio`, `iostat`, `perf`, YCSB, RocksDB, `numactl`, pinning helpers in `common/`.  
- **Drivers:** Intel QAT (QATlib) and device-specific drivers for DP-CSD/DPZip. Ensure driver version matches your kernel.

> **Power measurement:** CPU via RAPL; accelerators via vendor telemetry (QAT tools, DP-CSD APIs). If telemetry is unavailable, power-related figures will be marked **N/A**.

---

## 4) Kernel requirements (when and why)

Some figures rely on kernel features/behavior for QAT + filesystems.

- **Linux 6.9.0 + patch** — Required for **Btrfs** experiments (**Fig. 16, 17, 19b**).  
  Patch: `Figure_16-17-19b/linux6.9.0.patch`

  ```bash
  # Example flow (run on your build host)
  tar xf linux-6.9.0.tar.xz && cd linux-6.9.0
  patch -p1 < ../Figure_16-17-19b/linux6.9.0.patch
  make olddefconfig && make -j$(nproc)
  sudo make modules_install && sudo make install
  # Reboot into 6.9.0-patched and verify with: uname -r
  ```

- **Linux 5.15** — Used for **QAT 8970** experiments (**Fig. 8, 9, 19a**) due to driver support.  
- **Linux 6.5** — Default kernel for the rest (QAT 4xxx, SSD tests; any figure not listed above).

---

## 5) Reproduction matrix (figure → scripts → outputs → tolerance)

| Fig | Topic | Env | Entry point(s) | Primary outputs | Validation / tolerance |
|---|---|---|---|---|---|
| 2 | Zstd stage breakdown & parameter effects | CPU | `Figure_02/build_and_test.sh` → `draw.py` | `out/figure2.pdf\|png` | Stage shares & trends match; absolute times may vary ±20% |
| 7 | Ratio comparison (4 KB vs 64 KB) | CPU | `dpzip_vs_zstd_4k.py`, `dpzip_vs_zstd_64k.py` | `out/figure7_4k.png`, `out/figure7_64k.png` | Ratios within ±0.5 % absolute; ordering consistent |
| 8 | 4 KB throughput (CPU vs QAT/DPZip/DP-CSD) | HW | `Figure_08-09-19a/lzbench_test/run_lzbench*.sh` → `draw_figure8.py` | `out/figure8.png` | Within ±15 % of paper; trends preserved |
| 9 | 64 KB throughput | HW | same path as Fig.8, configured for 64 KB → `draw_figure9.py` | `out/figure9.png` | ±15 % |
| 11 | QAT latency breakdown (post-proc) | CPU (post) | `Figure_11/draw.py` | `out/figure11.png` | Component breakdown present; absolute ns may differ |
| 12 | Robustness vs. compressibility | CPU (post) | `Figure_12/draw.py` | `out/figure12.png` | DPZip drop <≈ expected threshold; shapes match |
| 14 | YCSB OPS scaling (RocksDB A/F) | HW | `Figure_14-15-20/run_all.sh` → `analyze_thrpt/*.py` → `draw_figure14.py` | `out/figure14.png` | Within ±15 % OPS; crossover points consistent |
| 15 | YCSB read latency | HW | `run_lat_test.sh` → `cal_ycsb/cal_avg_lat.py` → `draw_figure15.py` | `out/figure15.png` | ±15 % |
| 16,17 | Btrfs thr/lat (async comp + RA) | HW (6.9+patch) | `Figure_16-17-19b/version_CDF/*.sh` | `out/figure16.png`, `out/figure17.png` | ±15 % |
| 18 | ZFS latency vs record size | HW | `Figure_18/zfs_qat_test/run_test.sh` → `comp_ratio_test.sh` | `out/figure18.png` | ±15 % |
| 19a | Power (microbench, QAT 8970) | HW | `Figure_08-09-19a/*` + `collect_thrpt_and_power_verbose.py` | `out/figure19a.png` | ±20 % MB/J; ordering preserved |
| 19b | Power (Btrfs) | HW (6.9+patch) | `Figure_16-17-19b/draw_figure19ab.py` | `out/figure19b.png` | ±20 % MB/J |
| 20 | OPS/J (RocksDB+YCSB) | HW | `stats_aggr_workloada/print_each_task_power.py` → `draw_figure20.py` | `out/figure20.png` | ±20 % OPS/J |

> If your hardware lacks a device, the corresponding figure can be generated with the **available subsets**; missing series appear as **N/A**.

---

## 6) Determinism, pinning, and data

- **Seeds:** Scripts accept `AE_SEED` (default provided where relevant) for synthetic data.  
  Example: `AE_SEED=20250101 python dpzip_vs_zstd_64k.py`
- **CPU isolation:** Use our helpers (e.g., `common/pin.sh`, `numactl`) to pin workers to a socket and set the governor to `performance`.  
- **Background noise:** Close other workloads; disable turbo if you need tighter bounds; ensure cool/consistent thermals.  
- **Compression integrity:** All throughput tests perform **round-trip checks** (decompress == original). Failures abort the run.

---

## 7) Per-figure walkthrough (concise)

### Figure 2 — Zstd algorithm analysis (CPU-only)
```bash
cd Figure_02
cd zstd/build/cmake && cmake . && make
cd ../.. && ./test.sh
python draw.py
```

### Figure 7 — Ratio comparison (CPU-only)
```bash
cd Figure_07
python dpzip_vs_zstd_4k.py
python dpzip_vs_zstd_64k.py
```

### Figures 8 & 9 — Throughput @4 KB / @64 KB (hardware)
```bash
cd Figure_08-09-19a/lzbench_test
./run_lzbench.sh         # baseline
./run_lzbench_numa.sh    # NUMA-bound variant
cd ../peak_test/qat_8970 # or qat_4xxx/
# run the device-specific scripts, then:
cd ../../
python draw_figure8.py
python draw_figure9.py
```

### Figure 11 — QAT latency breakdown (post-proc)
```bash
cd Figure_11
python draw.py  # consumes telemetry exported from QAT tools
```

### Figure 12 — Robustness (plot-only)
```bash
cd Figure_12
python draw.py
```

### Figures 14, 15, 20 — RocksDB + YCSB
```bash
cd Figure_14-15-20
./run_all.sh                     # workload A/F throughput
./run_lat_test.sh                # latency runs
cd analyze_thrpt && python batch_collect.py && python cal_thrpt.py && cd ..
python draw_figure14.py
python cal_ycsb/cal_avg_lat.py
python draw_figure15.py
python stats_aggr_workloada/print_each_task_power.py
python draw_figure20.py
```

### Figures 16, 17, 19b — Btrfs (Linux 6.9.0 + patch)
```bash
# Boot the patched kernel first (see §4)
cd Figure_16-17-19b/version_CDF
./set_variables_new.sh
./run_throughput_test_CDF.sh
./stat_cpuutil_power.sh
cd ..
python draw_figure19ab.py
```

### Figure 18 — ZFS latency
```bash
cd Figure_18/zfs_qat_test
./run_test.sh
./comp_ratio_test.sh
```

---

## 8) Hardware/driver notes & fallbacks

- **Intel QAT**: Install QATlib matching your kernel; enable hugepages if recommended by your driver; ensure device nodes are present.  
- **DP-CSD / DPZip**: Load vendor drivers/modules and user-space libs per your board guide.  
- **Power**: If accelerator telemetry is unavailable, skip power figures (scripts will mark series **N/A**).

---

## 9) Common pitfalls (checklist)

- [ ] Kernel mismatch with QAT driver → device not enumerated.  
- [ ] CPU scaling governor not set to `performance` → noisy latency/throughput.  
- [ ] NUMA mis-pinning → underutilization.  
- [ ] Filesystem caching interference → follow the per-figure scripts that set mount options and drop caches where appropriate.  
- [ ] RAPL permissions → ensure access to `/sys/class/powercap/intel-rapl:*`.

---

## 10) Licensing, data, and ethics

- **License:** MIT for our code; third-party libs under their respective licenses (e.g., Zstd BSD).  
- **Data:** Synthetic data generators included; RocksDB/YCSB workloads produce non-sensitive data.  
- **Drivers/firmware:** Subject to vendor EULAs (QAT, DP-CSD/DPZip). We do not redistribute proprietary blobs.

---

## 11) Citation

If you use this artifact, please cite:

> _ASIC-based Compression Accelerators for Storage Systems: Design, Placement, and Profiling Insights._ EuroSys’26.  
> (Add DOI once available.)

```
@inproceedings{lu2026asiccompression,
  author    = {Tao Lu and Jiapin Wang and Yelin Shan and Xiangping Zhang and Xiang Chen},
  title     = {ASIC-based Compression Accelerators for Storage Systems: Design, Placement, and Profiling Insights},
  booktitle = {Proceedings of the European Conference on Computer Systems (EuroSys '26)},
  year      = {2026},
  month     = apr,
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  location  = {Edinburgh, Scotland, UK}
}
```

---

## 12) Support

Open an issue in this repository. When reporting results, include:
- OS + kernel (`uname -a`), CPU model, accelerator model/driver versions  
- Exact command lines used and the figure folder  
- The produced `out/*.json|csv|png` and any logs under `logs/`

---

### Appendix A — Minimal verification targets

- **CPU-only smoke:** Fig. 2 & Fig. 7 regenerate without hardware.  
- **QAT-only subset:** Fig. 8/9 + 11 + 18; 19a if telemetry available.  
- **Full hardware:** All figures including 16/17/19b (Btrfs, patched 6.9.0) and 14/15/20 (RocksDB+YCSB).

> Exact numeric equality is **not** required; we check **shape/order** and accept the tolerances in §5.

