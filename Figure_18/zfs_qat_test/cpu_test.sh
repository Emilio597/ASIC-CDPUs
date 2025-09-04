#!/bin/bash

num_runs=1
# 获取开始时间的精确时间戳（以纳秒为单位）
start_time=$(date +%s%N)

# 并发执行 ./turbobench 10 次
for i in $(seq 1 $num_runs); do
    /home/user/Programs/TurboBench/turbobench -elibdeflate,1 /home/user/Programs/zfs_qat_test/silesia.tar &
    echo start-$i
done

# 等待所有并发进程完成
wait

# 获取结束时间的精确时间戳（以纳秒为单位）
end_time=$(date +%s%N)

# 计算总耗时（结束时间减去开始时间，单位为秒）
elapsed_time=$(echo "scale=6; ($end_time - $start_time) / 1000000000" | bc)

# 获取文件的大小（以字节为单位）
file_size=$(stat -c%s "/home/user/Programs/zfs_qat_test/silesia.tar")

# 计算文件大小乘以并发次数，转换为兆字节（MB）
total_data_processed=$(echo "scale=6; ($file_size * $num_runs) / 1048576" | bc)

# 计算吞吐量（MB/s）
throughput=$(echo "scale=6; $total_data_processed / $elapsed_time" | bc)

# 输出结果
echo "Total time for $num_runs concurrent turbobench runs: $elapsed_time seconds"
echo "Total data processed: $total_data_processed MB"
echo "Throughput: $throughput MB/s"
