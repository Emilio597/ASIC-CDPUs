#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <log_file>"
    exit 1
fi


# 输入日志文件的路径
log_file="$1"

# 提取各个阶段的 kB_wrtn 值
load_start=$(grep -A 5 "Load Start" "$log_file" | grep "nvme0n1" | awk '{print $7}')
load_end=$(grep -A 6 "Load End" "$log_file" | grep "nvme0n1" | awk '{print $7}')
run_start=$(grep -A 6 "Run Start" "$log_file" | grep "nvme0n1" | awk '{print $7}')
run_end=$(grep -A 6 "Run End" "$log_file" | grep "nvme0n1" | awk '{print $7}')

# 输出提取到的 kB_wrtn 值
echo "Load Start kB_wrtn: $load_start"
echo "Load End kB_wrtn: $load_end"
echo "Run Start kB_wrtn: $run_start"
echo "Run End kB_wrtn: $run_end"

# # 计算各个阶段的 kB_wrtn 增加量
load_diff=$((load_end - load_start))
run_diff=$((run_end - run_start))

# # 输出计算的差异
echo "Load Stage Write Difference: $load_diff KB" >> $log_file
echo "Run Stage Write Difference: $run_diff KB" >> $log_file
