#!/bin/bash

# 设置并行执行的实例数量
num_instances=88

# 定义日志文件路径
output_log="output_lzbench.log"
time_log="timing_lzbench.log"
job_log="joblog_lzbench.txt"

# 清空旧的日志文件
> "$output_log"
> "$time_log"
> "$job_log"

# 定义要执行的命令的函数
run_instance() {
    local instance_id=$1
    local start_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 记录开始时间
    echo "Instance $instance_id started at $start_time" >> "$time_log"
    
    # 执行命令并将输出追加到 output_log
    #numactl --cpunodebind=1 --membind=1 ./lzbench/lzbench -b64 -ezlib,1 -i0,30 /home/user/DataFiles/silesia_data/silesia.tar >> "$output_log" 2>&1
    #numactl --cpunodebind=1 --membind=1 ./lzbench/lzbench -b64 -esnappy,1 -i30,0 /home/user/DataFiles/silesia_data/silesia.tar >> "$output_log" 2>&1
    numactl --cpunodebind=1 --membind=1 ./lzbench/lzbench -b64 -ezstd,1 -i30,0 /home/user/DataFiles/silesia_data/silesia.tar >> "$output_log" 2>&1    
# numactl --cpunodebind=0 ./lzbench/lzbench -b4 -esnappy,1 -i0,10 /home/user/DataFiles/silesia_data/google_zstd_compress_500MB.tar >> "$output_log" 2>&1
    
    local end_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 记录结束时间
    echo "Instance $instance_id finished at $end_time" >> "$time_log"
}

export -f run_instance
export output_log
export time_log
sync && echo 3 > /proc/sys/vm/drop_caches
# 使用 GNU Parallel 启动多个实例，并记录作业日志
# --joblog 记录每个作业的详细信息，包括启动和结束时间
parallel --jobs "$num_instances" --joblog "$job_log" run_instance {} ::: $(seq 1 "$num_instances")

# 合并 job_log 和 time_log（可选）
echo "All instances completed at $(date '+%Y-%m-%d %H:%M:%S')" >> "$time_log"

echo "所有实例已完成。详细日志如下："
echo "输出日志: $output_log"
echo "时间日志: $time_log"
echo "作业日志: $job_log"
