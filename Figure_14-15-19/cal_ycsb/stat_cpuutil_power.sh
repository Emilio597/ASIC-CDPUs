#!/bin/bash
set -e 

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: $0 <res_dir> <ramp_time> <test_mode>"
  exit 1
fi

echo "Start recodring cpuutil & power stat" 

res_dir=$1
ramp_time=$2
test_mode=$3

mkdir -p $res_dir
file_path=$res_dir/cpuutil_power_stat_${test_mode}
file_path_iotop="$res_dir/iotop_stat_${test_mode}"


sleep $((ramp_time))
ycsb_pid=$(pgrep ycsb | head -n 1)

if [ -z "$ycsb_pid" ]; then
    echo "ycsb is not running. Exiting monitoring script."
    exit 1
fi


sudo iotop -b -d 1 | grep --line-buffered -E '^Total|^Current' >> "$file_path_iotop" &
iotop_pid=$!

# 计数器初始化
count_2=0

while true; do
    sleep 1
    count_2=$((count_2 + 1))

    # 检查 ycsb 进程是否运行
    if ! ps -p "$ycsb_pid" > /dev/null; then
        echo "ycsb has stopped. Exiting monitoring script."
        break
    fi

    # 记录 CPU 使用率
    time=$(date "+%Y-%m-%d %H:%M:%S")
    cpu_util=$(top -b -n1 | awk '/%Cpu\(s\):/ {print $2, $4, $6}')
    echo "$time - CPU_Util $cpu_util" >> "$file_path"

    #### 每 2 秒记录功率信息
    # if (( count_2 >= 2 )); then
    #     # power=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk -F"|" '/^Power  /{print $5}')
    #     power=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk '/Power/ && !/Button/ && !/Power1/ && !/Power2/ {printf "%s %s %s ", $1, $(NF-1), $NF} END {print ""}')
    #     echo "$time - $power" >> "$file_path"
    #     count_2=0  # 重置计数器
    # fi
    power=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk '/Power/ && !/Button/ && !/Power1/ && !/Power2/ {printf "%s %s %s ", $1, $(NF-1), $NF} END {print ""}')
    echo "$time - $power" >> "$file_path"

done

# 停止 iotop 后台进程
kill "$iotop_pid" 2>/dev/null

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