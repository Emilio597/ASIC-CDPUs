#!/bin/bash

set -e

###### kernel 6.5.0
# param1_list=("NoComp" "ZLIB" "QAT-4XXX-1socket" "QAT-4XXX-2socket")
# param2_list=(5 10 15 20 25 30 40 50 60)

##### kernel 6.5.0

# param1_list=("QAT-4XXX-1socket" "QAT-4XXX-2socket" "NoComp" "ZLIB")
# param2_list=(5 10 15 20 25 30 40 50 60 70 90 120 150)
param1_list=("CSD")
param2_list=(10 20 30 40 50 60 70 80 88)


for param1 in "${param1_list[@]}"; do
    cmd="./lat_test.sh $param1"
    
    for i in {1..3}; do
        echo "Running: $cmd (Iteration $i)"
        eval $cmd
        sync && echo 3 > /proc/sys/vm/drop_caches
    done
done