#!/bin/bash
set -e

############# 参数设置
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] || [ -z "$6" ]; then
  echo "Input: $0 <task_name(qat-8970, qat-4xxx, cpu, csd, no-comp)> \
  <compression_option(no/zlib/zlib:1)> \
  <timestamp> \
  <ramp_time(70/30)> \
  <direct_io(1/0)> \
  <dev_name>"
  exit 1
fi

task_name=$1
compression_option=$2
timestamp=$3
ramp_time=$4 
direct_io=$5
dev_name=$6
size="500G"

# ✅ 打印所有参数
echo "====================="
echo "任务名称 (task_name)       : $task_name"
echo "压缩选项 (compression_option) : $compression_option"
echo "时间戳 (timestamp)        : $timestamp"
echo "预热时间 (ramp_time)      : $ramp_time"
echo "是否使用 Direct I/O (direct_io) : $direct_io"
echo "设备名称 (dev_name)       : $dev_name"
echo "测试数据大小 (size)       : $size"
echo "====================="

dev_name_wo_ns=${dev_name:0:10}

############# 挂载设备
if mount | grep -q -- "$dev_name"; then
    echo "$dev_name is mounted. Unmounting now..."
    
    # 卸载设备，确保 sudo 权限
    if sudo umount "$dev_name"; then
        echo "Unmounted successfully."
    else
        echo "Failed to unmount $dev_name."
        exit 1  # 直接终止脚本，并返回错误状态
    fi
else
    echo "$dev_name is not mounted. No action needed."
fi

mkfs.btrfs -f $dev_name
if [ "$task_name" == "csd" ] || [ "$task_name" == "no-comp" ]; then
    #CHANGED
    # mount -o compress=$compression_option,thread_pool=64,nodatasum $dev_name /home/user/mount_point/
    mount -o compress=$compression_option,thread_pool=64,datasum $dev_name /home/user/mount_point/
else
    #CHANGED
    # mount -o compress=$compression_option,thread_pool=64,nodatasum,compress-force $dev_name /home/user/mount_point/
    mount -o compress=$compression_option,thread_pool=64,datasum,compress-force $dev_name /home/user/mount_point/
fi
sync && echo 3 > /proc/sys/vm/drop_caches && sleep 1

if [ "$(ls -A /home/user/mount_point/)" ]; then
    echo "/home/user/mount_point/ is not empty. Deleting files..."
    rm -rf /home/user/mount_point/*
    echo "Files deleted."
else
    echo "/home/user/mount_point/ is already empty. No action needed."
fi

########## 设置结果日志路径
pwd_dir=`pwd`
res_dir=$pwd_dir/results/${task_name}/${timestamp}
mkdir -p $res_dir
res_file_path1=$res_dir/thrp_res1
conf_path=$res_dir/conf

###### 如果是SSD压缩，需要开启状态打印功能
if [ "$task_name" == "csd" ]; then
    nvme dapu dapudevelop $dev_name_wo_ns -c 0 -t 0xff -n `nvme dapu get-fwVerInfo $dev_name_wo_ns -H 2>&1 |  grep vendorSpecific | cut -d: -f 2`
    nvme dapu debug-command $dev_name_wo_ns -s "cps_stat show" >> $conf_path 2>&1
    echo "" >> $conf_path  
    nvme dapu get-selfDetailSmartInfo -H $dev_name |grep wr -i >> $conf_path 2>&1
    echo "" >> $conf_path  
    nvme dapu get-compressRatio $dev_name -t 1 -H >> $conf_path 2>&1
fi


######## 保存当前环境和读写命令执行信息
WRITE_COMMAND_CONF1="$pwd_dir/fio_config_file/write_test2.fio"
# WRITE_COMMAND1="fio --size=$size --fallocate=none --runtime=80 --direct=$direct_io --ramp_time=$ramp_time $WRITE_COMMAND_CONF1"
WRITE_COMMAND1="fio --size=$size --fallocate=none --direct=$direct_io --ramp_time=$ramp_time $WRITE_COMMAND_CONF1"


READ_COMMAND_CONF1="$pwd_dir/fio_config_file/read_test2.fio"


echo $(uname -r) >> $conf_path
echo $(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk '/Power/ && !/Button/ && !/Power1/ && !/Power2/ {print $1, $(NF-1), $NF}') >> $conf_path
echo $(ls /lib/modules/$kernel_version/kernel/drivers/crypto/intel/qat/qat_4xxx/) >> $conf_path
echo $(ls /lib/modules/$kernel_version/kernel/drivers/crypto/intel/qat/qat_c62x/) >> $conf_path
echo "compression_option=$compression_option" >> $conf_path

echo "WRITE_COMMAND1:$WRITE_COMMAND1" >> $conf_path
cat $WRITE_COMMAND_CONF1 >> $conf_path
echo "READ_COMMAND2:$READ_COMMAND2" >> $conf_path
cat $READ_COMMAND_CONF1 >> $conf_path



####### 执行命令并记录结果、功耗、压缩率
echo "#############################write###########################" >> $res_file_path1
sync && echo 3 > /proc/sys/vm/drop_caches && sleep 3
ssh localhost "$WRITE_COMMAND1 2>&1 | tee -a $res_file_path1" &
# $WRITE_COMMAND1 2>&1 | tee -a $res_file_path1 &
./stat_cpuutil_power.sh $task_name $timestamp $ramp_time "write"
wait
sync
echo "All WRITE tasks are done!"
compsize /home/user/mount_point/ 2>&1 | tee -a $res_file_path1
if [ "$task_name" == "csd" ]; then
    nvme dapu debug-command $dev_name_wo_ns -s "cps_stat show" >> $res_file_path1 2>&1
    echo "" >> $conf_path  
    nvme dapu get-selfDetailSmartInfo -H $dev_name |grep wr -i >> $res_file_path1 2>&1
    echo "" >> $conf_path  
    nvme dapu get-compressRatio $dev_name -t 1 -H >> $res_file_path1 2>&1
    echo "" >> $conf_path  
fi


echo "#############################read###########################" >> $res_file_path1
sync && echo 3 > /proc/sys/vm/drop_caches && sleep 5

start_rate=$((2000/6))
end_rate=$((8000/6))
step_rate=$((400/6))
current_rate=$((start_rate))

while [ $current_rate -le $end_rate ]
do
    echo "#####################################Running READ with rate limit: $((current_rate*6))MB/s#################################################" | tee -a $res_file_path1
    READ_COMMAND2="fio --rate=${current_rate}M --direct=$direct_io $READ_COMMAND_CONF1"

    for i in {1..3}
    do
        echo "##########Round $i for rate $((current_rate*6))MB/s##########" | tee -a $res_file_path1
        sync && echo 3 > /proc/sys/vm/drop_caches && sleep 2
        ssh localhost "$READ_COMMAND2 2>&1 | tee -a $res_file_path1"
    done
    # $READ_COMMAND2 2>&1 | tee -a $res_file_path1
    # ./stat_cpuutil_power.sh $task_name $timestamp 3 "read_${current_rate}MB"
    # wait
    sync

    current_rate=$((current_rate + step_rate))
done

echo "All READ tasks are done!"

