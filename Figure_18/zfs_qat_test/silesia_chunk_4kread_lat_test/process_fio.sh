#!/bin/bash

# 定义一个变量来保存总的延迟时间
total_latency=0
# 定义一个变量来计数处理的job数
job_count=0

# 读取fio输出内容
while IFS= read -r line; do
    # 检查当前行是否包含 "lat (nsec):"
    if [[ $line == *" lat (nsec):"* ]]; then
        # 提取出 avg 延迟时间，并确保没有多余的符号
        avg_latency=$(echo $line | awk -F'avg=' '{print $2}' | awk '{print $1}' | sed 's/,//g')

        # 检查 avg_latency 是否是数字
        if [[ $avg_latency =~ ^[0-9]+([.][0-9]+)?$ ]]; then
            echo "$avg_latency"

            # 将 avg_latency 添加到 total_latency 中，使用 bc 进行浮点运算
            total_latency=$(echo "$total_latency + $avg_latency" | bc)
            
            # 增加job计数
            job_count=$((job_count + 1))
        else
            echo "Warning: Invalid latency value found for Job $((job_count + 1))"
        fi
    fi
done

# 计算所有job的总体平均延迟
if [ $job_count -gt 0 ]; then
    overall_avg_latency=$(echo "scale=2; $total_latency / $job_count" | bc)
    echo "Overall Average Latency = $overall_avg_latency ns"
else
    echo "No jobs found."
fi
