#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <compression_option(no/zlib/zlib-1)> <task_name>"
  exit 1
fi

compression_option=$1
task_name=$2

dev_name=$(nvme list | grep SN-8D64763976E5018B | cut -c 1-12)
if mount | grep -q "$dev_name"; then
    echo "$dev_name is mounted. Proceeding to unmount."
    umount $dev_name
    echo "$dev_name has been unmounted."
else
    echo "$dev_name is not mounted. No action needed."
fi

# sudo nvme format $dev_name -l 2
mkfs.btrfs -f $dev_name


if [ "$task_name" == "csd" ] || [ "$task_name" == "no-comp" ]; then
    mount -o compress=$compression_option,thread_pool=64,nodatasum $dev_name /home/user/mount_point/
else
    mount -o compress=$compression_option,thread_pool=64,nodatasum,compress-force $dev_name /home/user/mount_point/
fi

cp /home/user/DataFiles/silesia_data/silesia.tar /home/user/mount_point/ && sync

sync && nvme list | grep $dev_name >> compress_stats.txt