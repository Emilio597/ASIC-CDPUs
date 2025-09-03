#!/bin/bash

RESULTS_DIR="./results"
FILE_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
RESULT_PATH="$RESULTS_DIR/$FILE_TIMESTAMP"
TRACE_DIR="./trace_dir"
rm -f $TRACE_DIR/*
nvme format /dev/nvme0n1

mkdir -p "$RESULT_PATH"

echo "[+] Running write test..."
sync && echo 3 > /proc/sys/vm/drop_caches
fio ./write_script.fio > "$RESULT_PATH/write"

# cat /sys/block/sfdv0n1/sfx_smart_features/sfx_capacity_stat > "$RESULT_PATH/compress_ratio_stat"
dev=/dev/nvme0;nvme dapu dapudevelop $dev -c 0 -t 0xff -n `nvme dapu get-fwVerInfo $dev -H 2>&1 | grep vendorSpecific | cut -d: -f 2`
nvme dapu debug-command /dev/nvme0 -s "cps_stat show" >> "$RESULT_PATH/compress_ratio_stat"
nvme dapu get-compressRatio /dev/nvme0n1 -t 1 -H >> "$RESULT_PATH/compress_ratio_stat"
nvme dapu get-selfDetailSmartInfo -H /dev/nvme0n1 | grep wr -i >> "$RESULT_PATH/compress_ratio_stat"

echo "[+] Modifying trace files (write → read)..."
for f in $TRACE_DIR/trace_*.log; do
  [ -f "$f" ] && sed -i 's/write/read/g' "$f"
done

echo "[+] Running read replay test..."
sync && echo 3 > /proc/sys/vm/drop_caches
fio ./read_script.fio > "$RESULT_PATH/read"



echo "[✓] All results saved to $RESULT_PATH"
