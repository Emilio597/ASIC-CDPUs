#!/bin/bash

# 定义所有压缩策略
task_9a_9b="9b"
# strategies=("no-comp" "cpu" "csd" "qat-4xxx" "qat-8970")
# strategies=("no-comp" "cpu" "qat-4xxx" "qat-8970")
# strategies=("no-comp" "cpu" "qat-4xxx")
strategies=("no-comp")



for mode in "${strategies[@]}"; do
  echo -e "\n==============================="
  echo "[🔥] 当前测试模式：$mode"
  echo "===============================\n"
  export TASK="$mode"
  # 设置环境变量（调用 set_variables.sh）
  source ./set_variables.sh

  # 输出当前测试信息
  echo "task_name=$task_name, \
    compression_option=$compression_option, \
    timestamp=$timestamp, \
    ramp_time=$ramp_time, \
    direct_io=$direct_io, \
    dev_name=$dev_name"

  if [ "$mode" = "cpu" ]; then
    bamsort_level=1
  else
    bamsort_level=0
  fi

  # 调用实际测试脚本
  ./run_throughput_test.sh "$task_name" \
    "$compression_option" \
    "$timestamp" \
    "$ramp_time" \
    "$direct_io" \
    "$dev_name" \
    "$bamsort_level" \
    "$task_9a_9b"

  echo -e "\n[✔️] $mode 模式测试完成\n"
done