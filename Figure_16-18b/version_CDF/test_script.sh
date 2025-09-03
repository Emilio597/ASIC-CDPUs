#!/bin/bash
set +x
####### qat-8970, qat-4xxx, cpu, csd, no-comp
# 定义所有压缩策略
# strategies=("no-comp" "cpu" "csd" "qat-4xxx" "qat-8970")
# strategies=("no-comp" "cpu" "qat-4xxx" "qat-8970")
# strategies=("qat-8970")
# strategies=("qat-4xxx" "no-comp" "cpu" "no-comp" "cpu" "qat-4xxx" "no-comp" "cpu" "qat-4xxx" "no-comp" "cpu" "qat-4xxx" "no-comp" "cpu" "qat-4xxx")
strategies=("qat-4xxx")


for mode in "${strategies[@]}"; do
    echo -e "\n==============================="
    echo "[🔥] 当前测试模式：$mode"
    echo "==============================="
    export TASK="$mode"
    # 设置环境变量（调用 set_variables.sh）
    source ./set_variables_new.sh

    # 输出当前测试信息
    echo "task_name=$task_name, \
        compression_option=$compression_option, \
        timestamp=$timestamp, \
        ramp_time=$ramp_time, \
        direct_io=$direct_io, \
        dev_name=$dev_name \
        kernel_version=$kernel_version"
    
    sync && echo 3 > /proc/sys/vm/drop_caches
    nvme format /dev/nvme0n1

    ./run_throughput_test_CDF.sh "$task_name" \
        "$compression_option" \
        "$timestamp" \
        "$ramp_time" \
        "$direct_io" \
        "$dev_name" \
        "$kernel_version"

    # ./run_write_lat_test.sh "$task_name" \
    # "$compression_option" \
    # "$timestamp" \
    # "$dev_name"


    # ./run_read_lat_test.sh "$task_name" \
    # "$compression_option" \
    # "$timestamp" \
    # "$dev_name"

    # ./get_compress_ratio.sh "$compression_option " \
    # "$task_name"
  echo -e "\n[✔️] $mode 模式测试完成\n"
done