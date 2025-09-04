#!/bin/bash

# 原始脚本路径

# available_mem_kb=$(free | awk '/Mem:/ {print $7}')
# available_mem_gb=$((available_mem_kb / 1024 / 1024))

# echo "available_mem_gb is: $available_mem_gb"
# # 判断可用内存是否大于 20GB
# if [ "$available_mem_gb" -gt 15 ]; then
#     echo "Available memory is greater than 20GB, executing commands..."
#     # 执行挂载和数据生成的命令
#     mount -o remount,size=108G /dev/shm
#     dd if=/dev/urandom of=/dev/shm/memory_block bs=108M count=1024
# else
#     echo "Available memory is less than or equal to 20GB, skipping commands."
# fi


# 原始脚本路径
script_path="./read_whole_big_file_params.sh"

# 第一个集合 (nocomp, qat, cpu, csd)
# first_set=("nocomp" "qat" "cpu" "csd")
# first_set=("cpu")

# # 第二个集合 (4K, 8K, 16K, 32K, 64K, 128K)
# second_set=("4K" "8K" "16K" "32K" "64K" "128K")

first_set=("qat")

# 第二个集合 (4K, 8K, 16K, 32K, 64K, 128K) "4K" "32K" 
second_set=("16K" "32K" "64K" "128K")

folder_time=$(date +"%m_%d-%H_%M")

read_iters=2

# 遍历两个集合的所有组合
for first_value in "${first_set[@]}"; do
    for blocksize in "${second_set[@]}"; do

        # 根据组合设置 compress_type
        if [[ "$first_value" == "nocomp" ]] || [[ "$first_value" == "csd" ]]; then
            compress_type="off"
        elif [[ "$first_value" == "qat" ]] || [[ "$first_value" == "cpu" ]]; then
            compress_type="gzip-1"
        else
            echo "Error: Unsupported compress_type for $first_value"
            exit 1
        fi

        # 根据组合设置 qat_disable
        if [[ "$first_value" == "qat" ]]; then
            qat_disable="0"
        else
            qat_disable="1"
        fi

        for i in {1..1}; do
            output_dir="./latency_res/$folder_time/${first_value}/${blocksize}"

            # 确保输出目录存在
            mkdir -p $output_dir

            echo "Running script with compress_type: $compress_type, blocksize: $blocksize, qat_disable: $qat_disable, read_iters: $read_iters"
            echo "Output will be saved to: $output_dir"

            # 调用原始脚本并传递参数组合和生成的文件名
            bash "$script_path" "$compress_type" "$blocksize" "$qat_disable" "$read_iters" "$output_dir"

            # 检查原脚本是否执行成功
            if [ $? -ne 0 ]; then
                echo "Error: Failed to execute script with compress_type: $compress_type, blocksize: $blocksize"
                exit 1
            fi

            echo "Completed execution with compress_type: $compress_type, blocksize: $blocksize"
        done
    done
done