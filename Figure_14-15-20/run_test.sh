#!/bin/bash

set -e

# 参数检查
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <task_name> <parallel_num>"
    exit 1
fi


task_name=$1
parallel_num=$2
dev_name=$3
WORKLOAD_TYPE=$4

YCSB_4XXX_PATH=/home/user/Programs/QAT-4xxx-suite/YCSB-cpp-4xxx
YCSB_8970_PATH=/home/user/Programs/QAT-8970-suite/YCSB-cpp-8970
MOUNT_POINT=/home/user/mount_point
RES_DIR=/home/user/Programs/YCSB-parallel-test/results
time_stamp=$(date +"%Y-%m-%d_%H-%M-%S")
OUT_DIR=/home/user/Programs/YCSB-parallel-test/results/$task_name/process_num_$parallel_num/$time_stamp---$WORKLOAD_TYPE
mkdir -p $OUT_DIR/load $OUT_DIR/run


### 挂载设备
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
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression="com.intel.qat_compressor_rocksdb"
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=com.intel.qat_compressor_rocksdb
                        "
    
    ;;

    "QAT-4XXX-2socket")
    ############# QAT-4xxx
    cp /home/user/Programs/QAT-4xxx-suite/etc_templates/etc_file_temp.conf /etc/4xxx_dev0.conf
    cp /home/user/Programs/QAT-4xxx-suite/etc_templates/etc_file_temp.conf /etc/4xxx_dev1.conf
    sleep 2
    systemctl restart qat
    sleep 2

    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression="com.intel.qat_compressor_rocksdb"
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=com.intel.qat_compressor_rocksdb
                        "
    
    ;;

    "QAT-8970")
    ############# QAT-8970
    cp /home/user/Programs/QAT-8970-suite/etc_templates/etc_file_temp.conf /etc/c6xx_dev0.conf
    cp /home/user/Programs/QAT-8970-suite/etc_templates/etc_file_temp.conf /etc/c6xx_dev1.conf
    cp /home/user/Programs/QAT-8970-suite/etc_templates/etc_file_temp.conf /etc/c6xx_dev2.conf
    
    sleep 2
    systemctl restart qat
    sleep 2
    
    YCSB_LOAD_COMMAND_PREFIX="$YCSB_8970_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_8970_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_8970_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression="com.intel.qat_compressor_rocksdb"
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_8970_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_8970_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_8970_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=com.intel.qat_compressor_rocksdb
                        "
    
    ;;
  "ZLIB")
    # ################ ZLIB
    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=zlib
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=zlib
                        "

    ;;
    "NoComp")
    ######### Non-Comp
    YCSB_LOAD_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -load \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=no
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
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
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
                        -P $YCSB_4XXX_PATH/rocksdb/rocksdb.properties \
                        -p rocksdb.compression=no
                        "

    YCSB_RUN_COMMAND_PREFIX="$YCSB_4XXX_PATH/ycsb \
                        -run \
                        -db rocksdb \
                        -P $YCSB_4XXX_PATH/workloads/$WORKLOAD_TYPE \
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
RUN_LOAD_POWER=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk '/Power/ && !/Button/ && !/Power1/ && !/Power2/ {printf "%s %s %s ", $1, $(NF-1), $NF} END {print ""}')
echo "RUN_LOAD_POWER: $RUN_LOAD_POWER" >> $OUT_DIR/iostat_record
echo "Load Start:" >> $OUT_DIR/iostat_record && iostat -d $dev_name >> $OUT_DIR/iostat_record
for i in $(seq 1 $parallel_num)
do
  YCSB_LOAD_COMMAND="systemd-run --scope -p MemoryLimit=2G $YCSB_LOAD_COMMAND_PREFIX \
  -p rocksdb.dbname=$MOUNT_POINT/ycsb-rocksdb_$i \
  -p measurementtype=hdrhistogram \
  -p recordcount=2000000 \
  -p operationcount=2000000 \
  -p requestdistribution=uniform \
  -p threadcount=10 \
  -p filename=/home/user/DataFiles/silesia_data/silesia.tar \
  -s"
  echo "Starting ycsb load process $i"
  # echo YCSB_LOAD_COMMAND:$YCSB_LOAD_COMMAND
  $YCSB_LOAD_COMMAND > $OUT_DIR/load/ycsb_load_$i.log 2>&1 &
done

wait 
sync && sleep 15 && sync
echo "All YCSB LOAD tasks finished."
echo "Load End:" >> $OUT_DIR/iostat_record && iostat -d $dev_name >> $OUT_DIR/iostat_record


sync && sleep 60
RUN_START_POWER=$(ipmitool -I lanplus -H 192.168.111.40 -U Administrator -P Admin@9000 sdr elist | awk '/Power/ && !/Button/ && !/Power1/ && !/Power2/ {printf "%s %s %s ", $1, $(NF-1), $NF} END {print ""}')
echo "RUN_START_POWER: $RUN_START_POWER" >> $OUT_DIR/iostat_record
echo "Run Start:" >> $OUT_DIR/iostat_record && iostat -d $dev_name >> $OUT_DIR/iostat_record

for i in $(seq 1 $parallel_num)
do
  YCSB_RUN_COMMAND="systemd-run --scope -p MemoryLimit=2G $YCSB_RUN_COMMAND_PREFIX \
  -p rocksdb.dbname=$MOUNT_POINT/ycsb-rocksdb_$i \
  -p measurementtype=hdrhistogram \
  -p recordcount=2000000 \
  -p operationcount=2000000 \
  -p requestdistribution=uniform \
  -p threadcount=10 \
  -p filename=/home/user/DataFiles/silesia_data/silesia.tar \
  -s"
  echo "Starting ycsb run process $i"
  # echo YCSB_RUN_COMMAND:$YCSB_RUN_COMMAND
  $YCSB_RUN_COMMAND > $OUT_DIR/run/ycsb_run_$i.log 2>&1 &
done

./cal_ycsb/stat_cpuutil_power.sh $OUT_DIR 3 run &

wait
sync && sleep 5 && sync
echo "All YCSB RUN tasks finished."
echo "Run End:" >> $OUT_DIR/iostat_record && iostat -d $dev_name >> $OUT_DIR/iostat_record



if [ "$task_name" == "CSD" ]; then
    nvme dapu get-compressRatio $dev_name -t 1 -H >> $OUT_DIR/iostat_record
fi
sync && echo 3 > /proc/sys/vm/drop_caches
umount $dev_name
sync && echo 3 > /proc/sys/vm/drop_caches

echo "All db_bench processes finished."

# ./cal_ycsb/run_cal.sh $OUT_DIR
