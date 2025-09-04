#!/bin/bash

# 输入文件名
input_file="fio_4k_lat_res.txt"

# 初始化总和变量
sum=0
count=0

# 处理 nsec 和 usec 的 avg 值
while read -r line; do
    # 匹配 nsec 和 usec 两种格式
    if [[ "$line" =~ lat\ \(nsec\)\: ]]; then
        # 提取 nsec 情况下的 avg 值，直接使用
        avg=$(echo "$line" | awk -F'avg=' '{print $2}' | cut -d',' -f1)
        # echo $avg
        sum=$(echo "$sum + $avg" | bc)
        ((count++))
    elif [[ "$line" =~ lat\ \(usec\)\: ]]; then
        # 提取 usec 情况下的 avg 值，并将其转换为 nsec（乘以1000）
        avg=$(echo "$line" | awk -F'avg=' '{print $2}' | cut -d',' -f1)
        avg_in_nsec=$(echo "$avg * 1000" | bc)
        # echo $avg_in_nsec
        sum=$(echo "$sum + $avg_in_nsec" | bc)
        ((count++))
    fi
done < "$input_file"

# 计算平均值
if [ "$count" -gt 0 ]; then
    average=$(echo "scale=2; $sum / $count" | bc)
    echo "平均值为: $average 纳秒"
else
    echo "没有找到任何 avg 值"
fi
