# #!/bin/bash

rm /home/user/Programs/zfs_qat_test/csd_mountpoint/*
sudo zfs unmount -f mypool/myfs
sudo zfs destroy mypool/myfs
sudo zpool destroy mypool

dev_name=$(nvme list | grep SN-8D64763976E5018B | cut -b 1-12)
dev_name=$dev_name

sudo zpool create -f mypool $dev_name
sudo zfs create mypool/myfs
sudo zfs set mountpoint=/home/user/Programs/zfs_qat_test/csd_mountpoint mypool/myfs
sudo zfs set compression=gzip-1 mypool/myfs
zfs set recordsize=256KB mypool/myfs
# sudo zfs set compression=off mypool/myfs


zfs_qat_status=$(cat /sys/module/zfs/parameters/zfs_qat_compress_disable)

# 判断参数值并设置 output_filename
if [ "$zfs_qat_status" -eq 0 ]; then
    output_filename="./cpu_util_res/fio_test_res_zfsQAT.txt"
elif [ "$zfs_qat_status" -eq 1 ]; then
    output_filename="./cpu_util_res/fio_test_res_zfsCPU.txt"
else
    echo "Unexpected value: $zfs_qat_status"
    exit 1
fi

cpu_record_interval=1
# fio_wcmd="fio --name=write_test --directory=/home/user/Programs/zfs_qat_test/csd_mountpoint/ --iodepth=1 --ioengine=libaio --direct=1 --numjobs=6 --size=10GB --rw=write --bs=202MB --buffer_pattern='/home/user/Programs/zfs_qat_test/silesia.tar'"
# fio_wcmd="dd if=/home/user/Programs/zfs_qat_test/silesia.tar of=/home/user/Programs/zfs_qat_test/csd_mountpoint/dd_test_file bs=4K count=51200"
# fio_wcmd="fio --name=write_test --directory=/home/user/Programs/zfs_qat_test/csd_mountpoint/ --iodepth=1 --ioengine=libaio --direct=1 --numjobs=128 --size=8kb --rw=write --bs=8kb --buffer_compress_percentage=10"
fio_wcmd="fio --name=write_test --directory=/home/user/Programs/zfs_qat_test/csd_mountpoint/ --iodepth=1 --ioengine=libaio --direct=1 --numjobs=6 --size=10GB --rw=write --bs=128KB --buffer_pattern='/home/user/Programs/zfs_qat_test/silesia.tar_128k'"


./cpu_stat.sh $cpu_record_interval $output_filename\_write $fio_wcmd
sync

# sleep 3
# sudo sync; echo 3 > /proc/sys/vm/drop_caches
# free -m
# sleep 3
# free -m 

# # fio_rcmd="fio --name=read_test --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/write_test.2.0 --iodepth=1 --ioengine=libaio --direct=1 --numjobs=1 --size=10GB --rw=read --bs=202MB"
# fio_rcmd="fio fio_read_multi.fio"
# ./cpu_stat.sh $cpu_record_interval $output_filename\_read $fio_rcmd


# rm /home/user/Programs/zfs_qat_test/csd_mountpoint/*
# sudo zfs unmount -f mypool/myfs
# sudo zfs destroy mypool/myfs
# sudo zpool destroy mypool















# sudo zpool create -f mypool $dev_name
# sudo zfs create mypool/myfs
# sudo zfs set mountpoint=/home/user/Programs/zfs_qat_test/csd_mountpoint mypool/myfs
# sudo zfs set compression=gzip-1 mypool/myfs


# # fio --name=write_test --directory=/home/user/Programs/zfs_qat_test/csd_mountpoint/ --iodepth=1 --ioengine=libaio --direct=1 --numjobs=6 --size=10GB --rw=write --bs=202MB --buffer_pattern=\'/home/user/Programs/zfs_qat_test/silesia.tar\'


# zfs_qat_status=$(cat /sys/module/zfs/parameters/zfs_qat_compress_disable)

# # 判断参数值并设置 output_filename
# if [ "$zfs_qat_status" -eq 0 ]; then
#     output_filename="fio_test_res_zfsQAT.txt"
# elif [ "$zfs_qat_status" -eq 1 ]; then
#     output_filename="fio_test_res_zfsCPU.txt"
# else
#     echo "Unexpected value: $zfs_qat_status"
#     exit 1
# fi

# cpu_record_interval=1
# fio_cmd="fio --name=write_test --directory=/home/user/Programs/zfs_qat_test/csd_mountpoint/ --iodepth=1 --ioengine=libaio --direct=1 --numjobs=6 --size=10GB --rw=write --bs=202MB --buffer_pattern='/home/user/Programs/zfs_qat_test/silesia.tar'"
# ./cpu_stat.sh $cpu_record_interval $output_filename $fio_cmd


# rm /home/user/Programs/zfs_qat_test/csd_mountpoint/*
# sudo zfs unmount -f mypool/myfs
# sudo zfs destroy mypool/myfs
# sudo zpool destroy mypool