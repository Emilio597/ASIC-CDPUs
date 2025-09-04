#!/bin/bash

# Usage: ./monitor_and_run.sh <cpu_record_interval> <output_filename> <command_to_run>

# 参数检查
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <cpu_record_interval> <output_filename> <command_to_run>"
    exit 1
fi

# 读取CPU监控参数和要执行的命令
interval=$1
output_file=$2
command_to_run="${@:3}"

# 定义CPU使用率记录函数
function record_cpu_usage {
    echo "Starting CPU usage recording..."
    exec 3>"$output_file"
    local i=0
    while true; do
        cpu_usage=$(top -b -d 1 -n 2 | grep "Cpu(s)" | tail -n 1 | awk '{print $2, $4}' | cut -f 1 -d "%")
        # cpu_usage=$(top 1 -b -n 1 | grep -E '^%Cpu4\s*:')
        echo "$((i * interval)) $cpu_usage" >&3
        sleep $interval
        ((i++))
    done
    exec 3>&-
}

# 后台启动CPU使用率记录
record_cpu_usage &
cpu_recorder_pid=$!

# 执行主命令
echo "Running command: $command_to_run"
# taskset -c 4 $command_to_run
$command_to_run
command_status=$?

# 停止CPU使用率记录
kill $cpu_recorder_pid
wait $cpu_recorder_pid 2>/dev/null

# 输出CPU记录进程的结束信息和主命令的退出状态
echo "CPU usage recording stopped."
echo "Command exited with status $command_status."

# 返回主命令的退出状态作为脚本的退出状态
exit $command_status