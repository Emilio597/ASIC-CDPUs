#!/bin/bash
set -e

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <dir_analyze>"
    exit 1
fi

# task_name=$1
# time_stamp=$2
# num_process=$3
# res_dir=/home/user/Programs/YCSB-parallel-test/results
dir_analyze=$1

# python3 cal_ycsb/cal_ycsb_thrpt_inaccurate.py --input_file_pattern "$dir_analyze/run/ycsb*" >> $dir_analyze/total_run_throuput
# python3 cal_ycsb/cal_avg_lat.py --input_file_pattern "$dir_analyze/run/ycsb*" >> $dir_analyze/total_run_throuput
cal_ycsb/cal_iostat_wrtn.sh $dir_analyze/iostat_record >> $dir_analyze/iostat_record