import os
import re
import sys
from datetime import datetime

if len(sys.argv) != 2:
    print(f"用法: python {sys.argv[0]} <顶层日志目录>")
    sys.exit(1)

top_level_dir = sys.argv[1]

# 匹配 process_num_XX 格式
process_pattern = re.compile(r"^process_num_(\d+)$")

# 匹配日志数据
runtime_pattern = re.compile(r"Run runtime\(sec\):\s*([\d.]+)")
operations_pattern = re.compile(r"Run operations\(ops\):\s*(\d+)")

# 匹配时间戳目录
def parse_timestamp(name):
    try:
        return datetime.strptime(name, "%Y-%m-%d_%H-%M-%S")
    except ValueError:
        return None

# 获取所有 process_num 目录并排序
process_dirs = []
for d in os.listdir(top_level_dir):
    full_path = os.path.join(top_level_dir, d)
    if os.path.isdir(full_path):
        m = process_pattern.match(d)
        if m:
            process_dirs.append((int(m.group(1)), full_path))

if not process_dirs:
    print("❌ 没有找到 process_num_XX 子目录")
    sys.exit(1)

process_dirs.sort(key=lambda x: x[0])  # 按进程数排序

# 遍历每个 process_num 目录
for process_num, proc_dir in process_dirs:
    # 找出最新的时间戳子目录
    timestamp_dirs = []
    for d in os.listdir(proc_dir):
        full_path = os.path.join(proc_dir, d)
        if os.path.isdir(full_path):
            ts = parse_timestamp(d)
            if ts:
                timestamp_dirs.append((ts, full_path))

    if not timestamp_dirs:
        print(f"⚠️  process_num_{process_num} 无有效时间戳子目录，跳过")
        continue

    latest_ts, latest_path = max(timestamp_dirs, key=lambda x: x[0])
    log_dir = os.path.join(latest_path, "run")

    print(f"\n📌 [process_num_{process_num}] 最新日志路径: {log_dir}")

    if not os.path.isdir(log_dir):
        print("❌ run/ 子目录不存在")
        continue

    # 解析日志文件
    total_throughput = 0.0
    found_any = False

    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        runtime_match = runtime_pattern.search(content)
        operations_match = operations_pattern.search(content)

        if runtime_match and operations_match:
            found_any = True
            runtime = float(runtime_match.group(1))
            operations = int(operations_match.group(1))

            if runtime > 0:
                throughput = operations / runtime
                total_throughput += throughput
                # print(f"   📄 {filename}: 吞吐量 = {throughput:.2f} ops/sec")

    if found_any:
        print(f"✅ [process_num_{process_num}] 总吞吐量: {total_throughput:.2f} ops/sec")
    else:
        print("⚠️  未能提取任何吞吐量信息")
