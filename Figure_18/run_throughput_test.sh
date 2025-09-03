#!/bin/bash
set -e

############# 参数设置
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] || [ -z "$6" ] || [ -z "$7" ] || [ -z "$7" ]; then
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
bamsort_level=$7
task_9a_9b=$8
size="400G"

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
if [ "$task_name" == "csd" ] || [ "$task_name" == "no-comp" ] || [ "$task_name" == "cpu" ]; then
    mount -o compress=$compression_option,thread_pool=64,nodatasum $dev_name /home/user/mount_point/
else
    mount -o compress=$compression_option,thread_pool=64,nodatasum,compress-force $dev_name /home/user/mount_point/
fi
sync && echo 3 > /proc/sys/vm/drop_caches && sleep 1

if [ "$(ls -A /home/user/mount_point/)" ]; then
    echo "/home/user/mount_point/ is not empty. Deleting files..."
    rm -rf /home/user/mount_point/*
    echo "Files deleted."
else
    echo "/home/user/mount_point/ is already empty. No action needed."
fi

###### 将BAM文件拷贝到挂载点
# cp -r /home/user/Programs/qzfs_test-xp/data /home/user/mount_point/
# sync; echo 3 > /proc/sys/vm/drop_caches


########## 设置结果日志路径
pwd_dir=`pwd`
res_dir=$pwd_dir/results/${task_9a_9b}/${task_name}/${timestamp}
mkdir -p $res_dir
# res_file_path=$res_dir/thrp_res
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
echo $(uname -r) >> $conf_path
echo "compression_option=$compression_option" >> $conf_path


####### 执行命令并记录结果、功耗、压缩率

if [ "$task_9a_9b" = "9a" ]; then
    cp /home/user/Programs/qzfs_test-xp/figure_9a_test/run_9a_bamsort.sh /home/user/mount_point/
    cd /home/user/mount_point
    /home/user/mount_point/run_9a_bamsort.sh $res_dir $bamsort_level
elif [ "$task_9a_9b" = "9b" ]; then
    cp /home/user/Programs/qzfs_test-xp/figure_9b_test/run_9b_bam.sh /home/user/mount_point/
    cd /home/user/mount_point
    /home/user/mount_point/run_9b_bam.sh $res_dir $bamsort_level
else
  echo "❌ 错误：未知任务类型 '$task_9a_9b'"
  exit 1
fi

# sync
# compsize -b /home/user/mount_point/sorted_t16.bam >> $conf_path
# echo "" >> $conf_path
# du /home/user/mount_point/sorted_t16.bam >> $conf_path
# echo "" >> $conf_path

wait
sync; echo 3 > /proc/sys/vm/drop_caches
echo "All READ tasks are done!"

