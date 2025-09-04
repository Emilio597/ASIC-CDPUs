#!/bin/bash
# set -e

# mount -o remount,size=108G /dev/shm
# dd if=/dev/urandom of=/dev/shm/memory_block bs=108M count=1024

# dev_name=$(nvme list | grep SN-8D64763976E5018B | cut -b 1-12)
dev_name=$(nvme list | grep SN-06A16F7C7C5B622D | cut -b 1-12)
dev_name=$dev_name

####### write file
rm /home/user/Programs/zfs_qat_test/csd_mountpoint/*
sudo zfs unmount -f mypool/myfs
sudo zfs destroy mypool/myfs
sudo zpool destroy mypool

sudo zpool create -f mypool $dev_name
sudo zfs create mypool/myfs
sudo zfs set mountpoint=/home/user/Programs/zfs_qat_test/csd_mountpoint mypool/myfs


echo 1 >> /sys/module/zfs/parameters/zfs_qat_compress_disable
sudo zfs set compression=off mypool/myfs

# sudo zfs set compression=gzip-1 mypool/myfs

#### close prefetch
echo 1 > /sys/module/zfs/parameters/zfs_prefetch_disable
# echo 1 > /sys/module/zfs/parameters/l2arc_noprefetch
# echo 1 > /sys/module/zfs/parameters/dmu_prefetch_max
# echo 1 > /sys/module/zfs/parameters/brt_zap_prefetch
# echo 1 > /sys/module/zfs/parameters/zap_iterate_prefetch
# echo 1 > /sys/module/zfs/parameters/zfs_no_scrub_prefetch
# echo 1 > /sys/module/zfs/parameters/zfs_arc_min_prefetch_ms
# echo 1 > /sys/module/zfs/parameters/zfs_arc_min_prescient_prefetch_ms
# echo 1 > /sys/module/zfs/parameters/zfs_send_no_prefetch_queue_ff
# echo 0 > /sys/module/zfs/parameters/zfs_send_no_prefetch_queue_length
# echo 0 > /sys/module/zfs/parameters/zfs_traverse_indirect_prefetch_limit
# echo 1 > /sys/module/zfs/parameters/zvol_prefetch_bytes

#### close cache
# echo 1 > /sys/module/zfs/parameters/dbuf_cache_hiwater_pct
# echo 1 > /sys/module/zfs/parameters/dbuf_cache_lowater_pct
# echo 1 > /sys/module/zfs/parameters/dbuf_cache_max_bytes
# echo 1 > /sys/module/zfs/parameters/dbuf_metadata_cache_max_bytes
# echo 0 > /sys/module/zfs/parameters/zfs_metaslab_max_size_cache_sec
# echo 1 > /sys/module/zfs/parameters/zfs_nocacheflush
# echo 1 > /sys/module/zfs/parameters/zil_nocacheflush
echo 268435456 > /sys/module/zfs/parameters/zfs_arc_max
echo 33554432 > /sys/module/zfs/parameters/zfs_arc_min
# echo 1 > /sys/module/zfs/parameters/zfs_arc_dnode_limit_percent
# echo 1 > /sys/module/zfs/parameters/l2arc_noprefetch
# echo 1 > /sys/module/zfs/parameters/l2arc_write_max




#############
zfs set recordsize=4K mypool/myfs
###############

cp /home/liwenjie/dapustor/large_silesia_file.tar /home/user/Programs/zfs_qat_test/csd_mountpoint/
# cp /home/user/Programs/zfs_qat_test/large_silesia_file.tar /home/user/Programs/zfs_qat_test/csd_mountpoint/

######### cgroup 
# sudo mkdir /sys/fs/cgroup/fio_limit
# echo $((400 * 1024 * 1024)) | sudo tee /sys/fs/cgroup/fio_limit/memory.max

echo "" > fio_4k_lat_res.txt
for i in {1..1}
do
    sync
    echo 1 > /proc/sys/vm/drop_caches

    sudo zfs unmount -f mypool/myfs
    sync
    echo 1 > /proc/sys/vm/drop_caches
    sudo zfs mount mypool/myfs

    sync
    echo 1 > /proc/sys/vm/drop_caches

    # fio --ioengine=libaio --name="align" --rw=randread --bs=4K --size=100% --io_size=4K --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar \
    # --direct=1 --iodepth=1 --offset=0 --group_reporting --numjobs=1 --norandommap \
    # --ba=256MB | grep "     lat (.*sec):"  >> fio_4k_lat_res.txt  

    # fio --ioengine=libaio --name="align" --rw=randread --bs=4K --size=100% --io_size=6% --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar \
    # --direct=1 --iodepth=1 --offset=0 --group_reporting --numjobs=1 --norandommap \
    # --ba=64K --output=fio_output1.log --continue_on_error=read
    # # | grep "     lat (.*sec):"  >> fio_4k_lat_res.txt 

    fio --ioengine=libaio --name="align" --rw=randread --bs=4K --size=100% --io_size=100%  --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar \
    --direct=1 --iodepth=1 --offset=0 --group_reporting --numjobs=1 --continue_on_error=read \
    --output=fio_output1.log --output-format=json
    # echo $! | sudo tee /sys/fs/cgroup/fio_limit/cgroup.procs

    wait
done
