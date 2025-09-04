#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

# === 路径配置 ===
BASE_DIR = "/home/user/Programs/YCSB-parallel-test/results"
OUTPUT_DIR = "/home/user/Programs/YCSB-parallel-test/analyze_thrpt/batch_outputs"
SCRIPT_PATH = "/home/user/Programs/YCSB-parallel-test/analyze_thrpt/collect_thrpt_and_power_verbose.py"

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 遍历 results 目录下的所有子目录
for entry in sorted(os.listdir(BASE_DIR)):
    full_path = os.path.join(BASE_DIR, entry)
    if not os.path.isdir(full_path):
        continue

    print(f"\n🟦 正在处理: {entry}...\n{'='*70}")
    log_path = os.path.join(OUTPUT_DIR, f"{entry}.log")

    try:
        # 执行分析脚本，捕获输出
        result = subprocess.run(
            ["python3", SCRIPT_PATH, full_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            check=False  # 避免异常中断
        )

        # 打印到控制台
        print(result.stdout)

        # 写入到日志文件
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"✅ 结果已保存至: {log_path}")

    except Exception as e:
        print(f"❌ 处理 {entry} 时出错: {e}")
