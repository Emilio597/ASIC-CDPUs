#!/bin/bash

set -e

###### kernel 6.5.0
# param1_list=("NoComp" "ZLIB" "QAT-4XXX-1socket" "QAT-4XXX-2socket")
# param2_list=(5 10 15 20 25 30 40 50 60)

##### kernel 6.5.0

# param1_list=("QAT-4XXX-1socket" "QAT-4XXX-2socket" "NoComp" "ZLIB")
# param2_list=(5 10 15 20 25 30 40 50 60 70 90 120 150)
# param1_list=("QAT-4XXX-2socket")
# param1_list=("NoComp" "ZLIB" )
# param1_list=("QAT-4XXX-2socket" "QAT-4XXX-2socket")
# param1_list=("CSD" "CSD" "CSD" "CSD" "CSD" "CSD" "CSD" "CSD" "CSD")
# param1_list=("ZLIB" "ZLIB" "ZLIB")
# param1_list=("NoComp" "NoComp" "NoComp")

param1_list=("QAT-8970")



param2_list=(1)
# param2_list=(10)

# param2_list=(50)

# param2_list=(50)

# dev_name=$(nvme list | grep SN-06A16F7C7C5B622D | cut -c 1-12)
dev_name=$(nvme list | grep RS6U04A23B00K6CQ | cut -c 1-12)
# dev_name=$(nvme list | grep RS6U0DA246010PP9 | cut -c 1-12)
# WORKLOAD_TYPE=workloadf # workloada workloadf


# for param1 in "${param1_list[@]}"; do
#     for param2 in "${param2_list[@]}"; do
#         for WORKLOAD_TYPE in workloada workloadf; do
#             cmd="./run_test.sh $param1 $param2 $dev_name $WORKLOAD_TYPE"
            
#             for i in {1..1}; do
#                 echo "Running: $cmd (Iteration $i)"
#                 eval $cmd
#                 sync && echo 3 > /proc/sys/vm/drop_caches
#             done
#         done
#     done
# done


for param1 in "${param1_list[@]}"; do
    # ✅ 根据 param1 设置 dev_name
    if [ "$param1" == "CSD" ]; then
        dev_name=$(nvme list | grep RS6U04A23B00K6CQ | cut -c 1-12)
    fi

    for param2 in "${param2_list[@]}"; do
        for WORKLOAD_TYPE in workloada workloadf; do
            cmd="./run_test.sh $param1 $param2 $dev_name $WORKLOAD_TYPE"

            for i in {1..1}; do
                echo "Running: $cmd (Iteration $i)"
                eval $cmd
                sync && echo 3 > /proc/sys/vm/drop_caches
            done
            find ./results/QAT-* -type f | parallel -j 170 "sed -i '/g_process\\.qz_init_status = QZ_NOSW_NO_HW/d;/Error userStarMultiProcess(-1), switch to SW if permitted/d;/\\[error\\] ADF_UIO_PROXY: icp_adf_userProcessToStart: Cannot open \\/dev\\/qat_dev_processes file/d' {}"
            
        done
    done
done

find ./results/QAT-* -type f | parallel -j 170 "sed -i '/g_process\\.qz_init_status = QZ_NOSW_NO_HW/d;/Error userStarMultiProcess(-1), switch to SW if permitted/d;/\\[error\\] ADF_UIO_PROXY: icp_adf_userProcessToStart: Cannot open \\/dev\\/qat_dev_processes file/d' {}"



# python3 recalculate_throghput_for_all_test.py
