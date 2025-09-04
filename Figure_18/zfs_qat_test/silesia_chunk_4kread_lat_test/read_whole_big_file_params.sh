#!/bin/bash
# set -e

iters=1


compress_type="$1"
blocksize="$2"
qat_disable="$3"
iters="$4"
output_dir="$5"


if [ -z "$compress_type" ] || [ -z "$blocksize" ] || [ -z "$output_dir" ] || [ -z "$qat_disable" ]; then
    echo "Usage: $0 <compression_type> <blocksize> <qat_disable> <iters> <output_dir>"
    exit 1
fi

dev_name=$(nvme list | grep SN-06A16F7C7C5B622D | cut -b 1-12)
dev_name=$dev_name

echo $dev_name

####### write file
sudo zfs destroy mypool/myfs
sudo zpool destroy mypool

sudo zpool create -f mypool $dev_name
zfs set recordsize=$blocksize mypool
sudo zfs create mypool/myfs
sudo zfs set mountpoint=/home/user/mnt/Programs/zfs_qat_test/csd_mountpoint mypool/myfs






#########zfs set

sudo zfs set compression=$compress_type mypool/myfs
sleep 1
zfs set recordsize=$blocksize mypool/myfs

# echo 268435456 > /sys/module/zfs/parameters/zfs_arc_max
# echo 33554432 > /sys/module/zfs/parameters/zfs_arc_min








# cp /home/liwenjie/dapustor/large_silesia_file.tar /home/user/Programs/zfs_qat_test/csd_mountpoint/
#cp /home/user/Programs/zfs_qat_test/large_silesia_file.tar /home/user/Programs/zfs_qat_test/csd_mountpoint/
cp /home/user/mnt/large_silesia_file.tar /home/user/Programs/zfs_qat_test/csd_mountpoint/


# echo "" > fio_4k_lat_res.txt
for i in $(seq 1 $iters)
do
    sync
    echo 1 > /proc/sys/vm/drop_caches
    sleep 1
    sudo zfs unmount -f mypool/myfs
    sleep 1
    sudo zpool export mypool
    sleep 1
    rmmod zfs
    sync
    echo 1 > /proc/sys/vm/drop_caches

    modprobe zfs
    sleep 1
    sudo zpool import mypool
    sync
    echo 1 > /proc/sys/vm/drop_caches

    timestamp=$(date +"%m_%d-%H_%M_%S")
    output_path="$output_dir/out_${timestamp}.txt"
    iolog_path="$output_dir/iolog_${timestamp}.txt"


    #########zfs set
    echo $qat_disable >> /sys/module/zfs/parameters/zfs_qat_compress_disable
    echo 1 > /sys/module/zfs/parameters/zfs_prefetch_disable



    # fio_command="fio --ioengine=psync --name=\"align\" --rw=randread --bs=4K --size=100% --io_size=5% --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar \
    # --direct=1 --iodepth=1 --offset=0 --group_reporting --numjobs=1 --output=$output_path --continue_on_error=read --randrepeat=0 --write_iolog=\"$iolog_path\""

    fio_command="fio --ioengine=psync --name=align --rw=randread --bs=4K --filename=/home/user/mnt/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar   --direct=1 --iodepth=1 --group_reporting --numjobs=1 --read_iolog=/home/user/mnt/iolog_128k.txt"

    echo "#############################################################" >> "$output_path"
    eval "$fio_command" >> "$output_path" 2>&1
    echo " " >> "$output_path"

    echo "zfs_prefetch_disable: $(cat /sys/module/zfs/parameters/zfs_prefetch_disable)" >> "$output_path"
    echo "zfs_arc_max_val: $(cat  /sys/module/zfs/parameters/zfs_arc_max)" >> "$output_path"
    echo "zfs_arc_min_val: $(cat  /sys/module/zfs/parameters/zfs_arc_min)" >> "$output_path"

    echo "zfs_qat_compress_disable: $(cat /sys/module/zfs/parameters/zfs_qat_compress_disable)" >> "$output_path"
    echo " " >> "$output_path"
    echo "compress_type: $(zfs get compression mypool/myfs)" >> "$output_path"
    echo " " >> "$output_path"
    echo "blocksize: $(zfs get recordsize mypool/myfs)" >> "$output_path"

    echo " " >> "$output_path"
    echo "iters: $iters" >> "$output_path"
    echo "output_path: $output_dir" >> "$output_path"

    wait
done