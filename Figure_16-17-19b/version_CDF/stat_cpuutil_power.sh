#!/bin/bash
set -e 

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: $0 <timestamp> <ramp_time> <test_mode>"
  exit 1
fi

echo "Start recodring cpuutil & power stat" 

task_name=$1
timestamp=$2
ramp_time=$3
test_mode=$4


res_dir=./results/${task_name}/${timestamp}
mkdir -p $res_dir
file_path=$res_dir/cpuutil_power_stat_${test_mode}
iotop_thrp_log=$res_dir/iotop_thrp_${test_mode}

sleep $((ramp_time+3))
fio_pid=$(pgrep -x fio | head -n 1)

if [ -z "$fio_pid" ]; then
    echo "fio is not running. Exiting monitoring script."
    exit 1
fi


# (
#     sleep 10  # 等待 10 秒
#     echo "" > $iotop_thrp_log  # 清空文件（可选，确保文件内容干净）
#     echo "Starting iotop monitoring..." >> $iotop_thrp_log

#     # 运行命令并将输出写入 iotop_thrp
#     iotop_counter_sec=0
#     while [ $iotop_counter_sec -lt 16 ]; do
#         if [ "$test_mode" == "write" ]; then
#             # 执行写模式监控命令
#             sudo iotop -n 2 -o -b | grep -E 'Total DISK WRITE|Current DISK WRITE' | tail -n 2 | \
#             awk -F'[:|]' '{gsub(/^[ \t]+|[ \t]+$/, "", $4); print $3 ": " $4}' | tr '\n' ',' | sed 's/,$/\n/' >> $iotop_thrp_log
#         elif [ "$test_mode" == "read" ]; then
#             # 执行读模式监控命令
#             sudo iotop -n 2 -o -b | grep -E 'Total DISK WRITE|Current DISK WRITE' | tail -n 2 | \
#             awk -F'[:|]' '{gsub(/^[ \t]+|[ \t]+$/, "", $4); print $1 ": " $2}' | tr '\n' ',' | sed 's/,$/\n/' >> $iotop_thrp_log
#         else
#             echo "Unknown test_mode: $test_mode" >> $iotop_thrp_log
#         fi

#         iotop_counter_sec=$((iotop_counter_sec+1))
#     done

#     echo "Stopping iotop monitoring..." >> $iotop_thrp_log
# ) &




# 计数器初始化
count_3=0
count_30=0
count_60=0

while true; do
    sleep 1
    count_3=$((count_3 + 1))
    count_30=$((count_30 + 1))

    # 检查 fio 进程是否运行
    if ! ps -p "$fio_pid" > /dev/null; then
        echo "fio has stopped. Exiting monitoring script."
        break
    fi

    # 记录 CPU 使用率
    time=$(date "+%Y-%m-%d %H:%M:%S")
    cpu_util=$(top -b -n1 | awk '/%Cpu\(s\):/ {print $2, $4, $6}')
    echo "$time - CPU_Util $cpu_util" >> "$file_path"

    # 每 5 秒记录功率信息
    if (( count_3 >= 1 )); then
        # power=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk -F"|" '/^Power  /{print $5}')
        power=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk '/Power/ && !/Button/ && !/Power1/ && !/Power2/ {printf "%s %s %s ", $1, $(NF-1), $NF} END {print ""}')
        echo "$time - $power" >> "$file_path"
        count_3=0  # 重置计数器
    fi

    # 每 20 秒记录负载信息
    if (( count_30 >= 30 )); then
        load_average=$(top -b -n1 | awk -F 'load average: ' '{print $2}' | awk -F ',' '{print $1}')
        echo "$time - Load_Average(1min): $load_average" >> "$file_path"
        count_30=0  # 重置计数器
    fi

done


calculate_average(){
    local temp_file="$1"  # 传入的文件路径
    local num_columns=$(head -n 1 "$temp_file" | awk '{print NF}')
    local sums=($(for i in $(seq 1 $num_columns); do echo 0; done))
    local count=0
    while read -r line; do
        local values=($line)
        for i in $(seq 0 $(($num_columns - 1))); do
            sums[$i]=$(echo "${sums[$i]} + ${values[$i]}" | bc)
        done
        count=$((count + 1))
    done < "$temp_file"

    local averages=()
    for sum in "${sums[@]}"; do
        averages+=($(echo "$sum / $count" | bc -l))
    done

    # 输出结果
    echo "${averages[@]}"
}


calculate_max(){
    local temp_file="$1"  # 传入的文件路径
    local num_columns=$(head -n 1 "$temp_file" | awk '{print NF}')
    local sums=($(for i in $(seq 1 $num_columns); do echo 0; done))
    local max_value=-inf
    local result_line=""
    while read -r line; do
        local values=($line)
        if (( $(echo "${values[$((num_columns-1))]} > $max_value" | bc -l) )); then
            max_value=${values[$((num_columns-1))]}
            result_line=("${values[@]}")
        fi
    done < "$temp_file"

    # 输出结果
    echo "${result_line[@]}"
}



############# get mean cpu utilization
input_file="$file_path" 
temp_file="tmp_file.txt"
> "$temp_file"  
grep "CPU_Util" "$input_file" | awk -F 'CPU_Util ' '{print $2}' >> "$temp_file"


avg_res=$(calculate_average "$temp_file")
avg_res=($avg_res)
for i in ${!avg_res[@]}; do
    echo "CPU_Avg_Utilization_Stats: Column $((i + 1)) average: ${avg_res[$i]}" >> "$file_path"
done
rm "$temp_file"


############# get max cpu power
temp_file="tmp_file.txt"
> "$temp_file" 
grep -E "CPU [0-9]+ Watts" "$input_file" | awk '{for (i=5; i<=NF; i++) if ($i ~ /^[0-9]+$/) printf "%s ", $i; print ""}' >> "$temp_file"

max_line_res=$(calculate_max "$temp_file")
max_line_res=($max_line_res)
for i in ${!max_line_res[@]}; do
    echo "CPU_Max_Power_Line_Stats: Column $((i + 1)) max: ${max_line_res[$i]}" >> "$file_path"
done

############### get avg cpu power
avg_res=$(calculate_average "$temp_file")
avg_res=($avg_res)
echo "Average CPU Power:"
for i in ${!avg_res[@]}; do
    echo "CPU_Avg_Power_Stats: Column $((i + 1)) average: ${avg_res[$i]}" >> "$file_path"
done

rm "$temp_file"