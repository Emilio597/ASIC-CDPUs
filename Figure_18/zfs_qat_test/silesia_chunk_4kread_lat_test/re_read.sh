echo "" > fio_4k_lat_res.txt
for i in {1..1}
do
    sync
    echo 3 > /proc/sys/vm/drop_caches

    sudo zfs unmount -f mypool/myfs
    sync
    echo 3 > /proc/sys/vm/drop_caches
    sudo zfs mount mypool/myfs

    sync
    echo 3 > /proc/sys/vm/drop_caches

    # fio --ioengine=libaio --name="align" --rw=randread --bs=4K --size=100% --io_size=4K --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar \
    # --direct=1 --iodepth=1 --offset=0 --group_reporting --numjobs=1 --norandommap \
    # --ba=256MB | grep "     lat (.*sec):"  >> fio_4k_lat_res.txt  

    fio --ioengine=libaio --name="align" --rw=randread --bs=4K --size=100%  --filename=/home/user/Programs/zfs_qat_test/csd_mountpoint/large_silesia_file.tar \
    --direct=1 --iodepth=1 --offset=0 --group_reporting --numjobs=1 --write_iolog=io_trace.log | grep "     lat (.*sec):"  >> fio_4k_lat_res.txt 
    # echo $! | sudo tee /sys/fs/cgroup/fio_limit/cgroup.procs

    wait
done