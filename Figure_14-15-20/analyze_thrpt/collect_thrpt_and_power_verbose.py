#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_thrpt_power_iostat.py

每个时间戳---workloadX目录：
  ✓ 汇总 run/ 中日志得总吞吐量（ops/sec）
  ✓ 提取 cpuutil_power_stat_run 的 Column 4 average 作为平均功耗
  ✓ 提取 iostat_record 的 RUN_START_POWER 行中的 Power 字段作为起始功耗
  ✓ 计算功耗差值 Δ = AvgPwr - StartPwr
  ✓ 打印实时进度和最终汇总结果
"""

import os
import re
import sys
from collections import defaultdict
from datetime import datetime

if len(sys.argv) != 2:
    print(f"用法: python {sys.argv[0]} <顶层日志目录>")
    sys.exit(1)

root_dir = sys.argv[1]

# ---------- 正则 ---------- #
process_pat     = re.compile(r"^process_num_(\d+)$")
ts_wl_pat       = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})---(?P<wl>workload\w+)$")
runtime_pat     = re.compile(r"Run runtime\(sec\):\s*([\d.]+)")
ops_pat         = re.compile(r"Run operations\(ops\):\s*(\d+)")
power_avg_pat   = re.compile(r"CPU_Avg_Power_Stats:\s*Column\s*4\s*average:\s*([\d.]+)")
iostat_power_pat= re.compile(r"RUN_START_POWER:.*Power\s+(\d+)\s+Watts", re.IGNORECASE)

# ---------- 结果容器 ---------- #
results: dict[str, list] = defaultdict(list)

# ---------- 工具函数 ---------- #
def scan_run_dir(run_dir: str) -> float:
    thrpt_sum = 0.0
    for entry in os.scandir(run_dir):
        if not entry.is_file():
            continue
        runtime = ops = None
        try:
            with open(entry.path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if runtime is None:
                        m = runtime_pat.search(line)
                        if m:
                            runtime = float(m.group(1))
                            if ops is not None:
                                break
                    if ops is None:
                        m = ops_pat.search(line)
                        if m:
                            ops = int(m.group(1))
                            if runtime is not None:
                                break
        except OSError:
            continue

        if runtime and ops and runtime > 0:
            thrpt_sum += ops / runtime
    return thrpt_sum

def parse_avg_power(path: str) -> float | None:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = power_avg_pat.search(line)
                if m:
                    return float(m.group(1))
    except OSError:
        pass
    return None

def parse_iostat_power(path: str) -> int | None:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = iostat_power_pat.search(line)
                if m:
                    return int(m.group(1))
    except OSError:
        pass
    return None

# ---------- 主流程 ---------- #
for proc_entry in os.scandir(root_dir):
    if not proc_entry.is_dir():
        continue
    m_proc = process_pat.match(proc_entry.name)
    if not m_proc:
        continue
    proc_num = int(m_proc.group(1))

    for sub_entry in os.scandir(proc_entry.path):
        if not sub_entry.is_dir():
            continue
        m_ts = ts_wl_pat.match(sub_entry.name)
        if not m_ts:
            continue

        ts      = datetime.strptime(m_ts.group("ts"), "%Y-%m-%d_%H-%M-%S")
        wl_name = m_ts.group("wl")
        run_dir = os.path.join(sub_entry.path, "run")
        if not os.path.isdir(run_dir):
            continue

        thrpt = scan_run_dir(run_dir)
        avg_power = parse_avg_power(os.path.join(sub_entry.path, "cpuutil_power_stat_run"))
        iostat_power = parse_iostat_power(os.path.join(sub_entry.path, "iostat_record"))

        if thrpt == 0.0:
            print(f"⚠️ Empty  {wl_name:<10} [process_num_{proc_num}] {sub_entry.name}")
            continue

        results[wl_name].append((proc_num, ts, thrpt, avg_power, iostat_power))

        pw_str = f"{avg_power:.2f} W" if avg_power is not None else "N/A"
        io_pw  = f"{iostat_power} W" if iostat_power is not None else "N/A"
        diff_str = (
            f"{avg_power - iostat_power:.2f} W"
            if avg_power is not None and iostat_power is not None else "N/A"
        )

        print(
            f"✓ 收到  {wl_name:<10} [process_num_{proc_num}] {sub_entry.name}  "
            f"{thrpt:,.2f} ops/s  AvgPwr: {pw_str}, StartPwr: {io_pw}, Δ: {diff_str}"
        )

# ---------- 汇总输出 ---------- #
if not results:
    print("❌ 没找到任何有效数据")
    sys.exit(0)

for wl in sorted(results.keys()):
    print(f"\n🔸 {wl}")
    sorted_group = sorted(results[wl], key=lambda x: (x[0], x[1]))
    last_proc = None

    for proc, ts, thr, avg_pwr, io_pwr in sorted_group:
        if proc != last_proc and last_proc is not None:
            print("   " + "-" * 75)
        last_proc = proc

        ts_str = ts.strftime("%Y-%m-%d_%H-%M-%S")
        avg_pwr_str = f"{avg_pwr:,.2f} W" if avg_pwr is not None else "N/A"
        io_pwr_str  = f"{io_pwr:>3} W" if io_pwr is not None else "N/A"
        diff_str = (
            f"{avg_pwr - io_pwr:,.2f} W"
            if avg_pwr is not None and io_pwr is not None else "N/A"
        )

        print(
            f"   [process_num_{proc:>2}] {ts_str}  "
            f"{thr:>12,.2f} ops/sec  "
            f"AvgPwr: {avg_pwr_str}, StartPwr: {io_pwr_str}, Diff: {diff_str}"
        )
