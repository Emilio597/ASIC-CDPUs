#!/bin/bash

# 设置并行执行的实例数量
num_instances=44

# 定义日志文件路径
output_log="output_lzbench.log"
time_log="timing_lzbench.log"
job_log="joblog_lzbench.txt"
target_file="/home/user/DataFiles/silesia_data/silesia.tar"

# 清空旧日志
> "$output_log"
> "$time_log"
> "$job_log"

# 定义单个实例执行函数
run_instance() {
    local instance_id=$1
    local start_time=$(date '+%Y-%m-%d %H:%M:%S')


    if (( instance_id <= 22 )); then
        numa_node=0
        cpunodebind=0
        physcpubind="1-43,88-131"
    else
        numa_node=1
        cpunodebind=1
        physcpubind="45-87,132-175"
    fi

    echo "Instance $instance_id (NUMA $numa_node) started at $start_time" >> "$time_log"

    # 执行绑定 NUMA 的 lzbench，并将输出写入统一日志
    numactl --cpunodebind=$cpunodebind --membind=$numa_node \
      ./lzbench/lzbench -b64 -esnappy,1 -i0,10 -p3 "$target_file" >> "$output_log" 2>&1
    # numactl --cpunodebind=$cpunodebind --membind=$numa_node \
    #   ./lzbench/lzbench -b64 -esnappy,1 -i1,2 -p3 "$target_file" >> "$output_log" 2>&1

    local end_time=$(date '+%Y-%m-%d %H:%M:%S')
    echo "Instance $instance_id (NUMA $numa_node) finished at $end_time" >> "$time_log"
}

export -f run_instance
export output_log
export time_log
export target_file

# 清缓存，避免 page cache 干扰


# 并行执行任务
parallel --jobs "$num_instances" --joblog "$job_log" run_instance {} ::: $(seq 1 "$num_instances")

# 合并时间记录
echo "All instances completed at $(date '+%Y-%m-%d %H:%M:%S')" >> "$time_log"

# 打印结果提示
echo "✅ 所有实例已完成。详细日志如下："
echo "📝 输出日志: $output_log"
echo "⏱️ 时间日志: $time_log"
echo "📄 作业日志: $job_log"
