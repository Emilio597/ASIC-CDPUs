#!/bin/bash

set -e
# 设置并行执行的实例数量
# num_instances=43

# export CPU_CORES_STRING="45 46 47 48 49 50 51 52 53 54 \
# 55 56 57 58 59 60 61 62 63 64 \
# 65 66 67 68 69 70 71 72 73 74 \
# 75 76 77 78 79 80 81 82 83 84 \
# 85 86 87 132 133 134 135 136 137 \
# 138 139 140 141 142 143 144 145 146 \
# 147 148 149 150 151 152 153 154 155 \
# 156 157 158 159 160 161 162 163 164 \
# 165 166 167 168 169 170 171 172 173 \
# 174 175"

num_instances=86

export CPU_CORES_STRING="45 45 46 46 47 47 48 48 49 49 \
50 50 51 51 52 52 53 53 54 54 \
55 55 56 56 57 57 58 58 59 59 \
60 60 61 61 62 62 63 63 64 64 \
65 65 66 66 67 67 68 68 69 69 \
70 70 71 71 72 72 73 73 74 74 \
75 75 76 76 77 77 78 78 79 79 \
80 80 81 81 82 82 83 83 84 84 \
85 85 86 86 87 87 132 132 133 133 \
134 134 135 135 136 136 137 137 \
138 138 139 139 140 140 141 141 \
142 142 143 143 144 144 145 145 \
146 146 147 147 148 148 149 149 \
150 150 151 151 152 152 153 153 \
154 154 155 155 156 156 157 157 \
158 158 159 159 160 160 161 161 \
162 162 163 163 164 164 165 165 \
166 166 167 167 168 168 169 169 \
170 170 171 171 172 172 173 173 \
174 174 175 175"



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
    local -a cpu_cores=($CPU_CORES_STRING)
    local cpu_core=${cpu_cores[$((instance_id - 1))]}
    local start_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 记录开始时间
    echo "Instance $instance_id started at $start_time" >> "$time_log"
    # echo "Instance $instance_id using CPU $cpu_core" >> "$output_log"

    # 执行命令并将输出追加到 output_log

    # numactl --physcpubind=$cpu_core --membind=1 ./lzbench/lzbench -b64 -esnappy,1 -i0,30 /home/user/DataFiles/silesia_data/silesia.tar >> "$output_log" 2>&1
    # numactl --cpunodebind=0 ./lzbench/lzbench -b4 -esnappy,1 -i0,10 /home/user/DataFiles/silesia_data/google_zstd_compress_500MB.tar >> "$output_log" 2>&1

    taskset -c "$cpu_core" numactl --membind=1 ./lzbench/lzbench -b4 -esnappy,1 -i30,30 /home/user/DataFiles/silesia_data/silesia.tar >> "$output_log" 2>&1
    # taskset -c "$cpu_core" numactl --membind=1 ./lzbench/lzbench -b4 -esnappy,1 -i10,0 /home/user/DataFiles/silesia_data/google_zstd_compress_500MB.tar >> "$output_log" 2>&1
    # taskset -c "$cpu_core" ./lzbench/lzbench -b4 -ezlib,1 -i20,20 /home/user/DataFiles/silesia_data/google_zstd_compress_500MB.tar >> "$output_log" 2>&1

    
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
