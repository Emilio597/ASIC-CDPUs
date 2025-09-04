import os
import re
import sys

if len(sys.argv) != 2:
    print(f"用法: python {sys.argv[0]} <日志目录路径>")
    sys.exit(1)

log_dir = sys.argv[1]
total_throughput = 0.0
log_dir=log_dir+"/run"
runtime_pattern = re.compile(r"Run runtime\(sec\):\s*([\d.]+)")
operations_pattern = re.compile(r"Run operations\(ops\):\s*(\d+)")

for filename in os.listdir(log_dir):
    file_path = os.path.join(log_dir, filename)
    if not os.path.isfile(file_path):
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        runtime_match = runtime_pattern.search(content)
        operations_match = operations_pattern.search(content)

        if runtime_match and operations_match:
            runtime = float(runtime_match.group(1))
            operations = int(operations_match.group(1))

            if runtime > 0:
                throughput = operations / runtime
                total_throughput += throughput
                print(f"{filename}: 吞吐量 = {throughput:.2f} ops/sec")

print(f"✅ 总吞吐量（各日志文件的吞吐量和）: {total_throughput:.2f} ops/sec")
