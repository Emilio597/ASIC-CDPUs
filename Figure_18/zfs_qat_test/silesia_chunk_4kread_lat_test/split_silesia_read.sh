#!/bin/bash

rm /home/user/Programs/zfs_qat_test/csd_mountpoint/*
sudo zfs unmount -f mypool/myfs
sudo zfs destroy mypool/myfs
sudo zpool destroy mypool

dev_name=$(nvme list | grep SN-8D64763976E5018B | cut -b 1-12)
dev_name=$dev_name

sudo zpool create -f mypool $dev_name
sudo zfs create mypool/myfs
sudo zfs set mountpoint=/home/user/Programs/zfs_qat_test/csd_mountpoint mypool/myfs
# sudo zfs set compression=gzip-1 mypool/myfs
sudo zfs set compression=off mypool/myfs



SOURCE_FILE="/home/user/Programs/zfs_qat_test/silesia.tar"
# Target directory
TARGET_DIR="/home/user/Programs/zfs_qat_test/csd_mountpoint"
# Block size
BLOCK_SIZE=$((17663146))
# Count of blocks to read (1 for 4KB each time)
COUNT=1

# Calculate the number of blocks in the source file
FILE_SIZE=$(stat --format=%s "$SOURCE_FILE")
NUM_BLOCKS=$((FILE_SIZE / BLOCK_SIZE))

for (( i=0; i<NUM_BLOCKS; i++ )); do
    # Use dd to read each 4KB block and write it to a separate file
    dd if="$SOURCE_FILE" of="$TARGET_DIR/file_$i.bin" bs=$BLOCK_SIZE count=$COUNT skip=$i
done

echo "Finished splitting $SOURCE_FILE into $NUM_BLOCKS files of $BLOCK_SIZE bytes each."

sync
echo 3 > /proc/sys/vm/drop_caches


sudo zfs unmount -f mypool/myfs
sudo zfs mount mypool/myfs

sync
echo 3 > /proc/sys/vm/drop_caches

fio ./fio_read_conf.fio > fio_output.txt
bash process_fio.sh < fio_output.txt