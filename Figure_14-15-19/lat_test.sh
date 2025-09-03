#!/bin/bash

set -e

# 参数检查
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <task_name> <parallel_num>"
    exit 1
fi


task_name=$1
parallel_num=1


YCSB_4XXX_PATH=/home/user/Programs/QAT-4xxx-suite/YCSB-cpp-4xxx
YCSB_8970_PATH=/home/user/Programs/QAT-8970-suite/YCSB-cpp-8970
MOUNT_POINT=/home/user/mount_point
RES_DIR=/home/user/Programs/YCSB-parallel-test/results
time_stamp=$(date +"%Y-%m-%d_%H-%M-%S")
OUT_DIR=$RES_DIR/latency/$task_name/$time_stamp
mkdir -p $OUT_DIR


# dev_name=$(nvme list | grep SN-8D64763976E5018B | cut -c 1-12)
dev_name=$(nvme list | grep SN-06A16F7C7C5B622D | cut -c 1-12)

### umount
if mount | grep -q "$dev_name"; then
  echo "$dev_name is mounted. Unmounting now..."
  umount $dev_name
  if [ $? -eq 0 ]; then
    echo "Unmounted successfully."
  else
    echo "Failed to unmount $dev_name."
  fi
else
  echo "$dev_name is not mounted. No action needed."
fi


mkfs.ext4 -F $dev_name
mount $dev_name $MOUNT_POINT

case "$task_name" in
    "QAT-4XXX-1socket")
    ############# QAT-4xxx
    if [ -f /etc/4xxx_dev1.conf ]; then
      rm -f /etc/4xxx_dev1.conf
    fi
    systemctl restart qat

    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression="com.intel.qat_compressor_rocksdb"
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=com.intel.qat_compressor_rocksdb
                        "
    
    ;;

    "QAT-4XXX-2socket")
    ############# QAT-4xxx
    cp /home/user/Programs/QAT-4xxx-suite/etc_templates/etc_file_temp.conf /etc/4xxx_dev1.conf
    systemctl restart qat

    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression="com.intel.qat_compressor_rocksdb"
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=com.intel.qat_compressor_rocksdb
                        "
    
    ;;

    "QAT-8970")
    ############# QAT-8970
    systemctl restart qat
    YCSB_LOAD_COMMAND_PREFIX="$YCSB_8970_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_8970_PATH/workloads/workloada \
                        -P $YCSB_8970_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression="com.intel.qat_compressor_rocksdb"
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_8970_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_8970_PATH/workloads/workloada \
                        -P $YCSB_8970_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=com.intel.qat_compressor_rocksdb
                        "
    
    ;;
  "ZLIB")
    # ################ ZLIB
    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=zlib
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=zlib
                        "

    ;;
    "NoComp")
    ######### Non-Comp
    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=no
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=no
                        "
    ;;

    "CSD")
    ######### CSD
    nvme dapu dapudevelop $dev_name -c 0 -t 0xff -n `nvme dapu get-fwVerInfo $dev_name -H 2>&1 | grep vendorSpecific | cut -d: -f 2`

    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=no
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/workloada \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=no
                        "
    ;;
  *)
  echo "Usage: $0 {QAT-4XXX-{?}socket | QAT-8970 | ZLIB | NoComp}"
  exit 1
  ;;
esac

sync && echo 3 > /proc/sys/vm/drop_caches

for i in $(seq 1 $parallel_num)
do
  YCSB_LOAD_COMMAND="systemd-run --scope -p MemoryLimit=10G $YCSB_LOAD_COMMAND_PREFIX -p recordcount=2000000 -p requestdistribution=uniform -p fieldlength=100 -p rocksdb.dbname=$MOUNT_POINT/ycsb-rocksdb_$i -s"
  echo "Starting ycsb load process $i"
  # echo YCSB_LOAD_COMMAND:$YCSB_LOAD_COMMAND
  $YCSB_LOAD_COMMAND > $OUT_DIR/load_lat_res 2>&1 &
done

wait 
sync && echo 3 > /proc/sys/vm/drop_caches
sync && sleep 15 && sync
sync && echo 3 > /proc/sys/vm/drop_caches
echo "All YCSB LOAD tasks finished."



sync


for i in $(seq 1 $parallel_num)
do
  YCSB_RUN_COMMAND="systemd-run --scope -p MemoryLimit=400M $YCSB_RUN_COMMAND_PREFIX -p operationcount=200000 -p requestdistribution=uniform -p fieldlength=100 -p rocksdb.dbname=$MOUNT_POINT/ycsb-rocksdb_$i -s"
  echo "Starting ycsb run process $i"
  # echo YCSB_RUN_COMMAND:$YCSB_RUN_COMMAND
  $YCSB_RUN_COMMAND > $OUT_DIR/run_lat_res 2>&1 &
done



wait

echo "All YCSB RUN tasks finished."
sync && echo 3 > /proc/sys/vm/drop_caches
umount $dev_name
sync && echo 3 > /proc/sys/vm/drop_caches

echo "All db_bench processes finished."
