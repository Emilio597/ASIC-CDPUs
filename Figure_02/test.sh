#!/bin/bash

# 定义文件列表
files=("ent1_128k.bin" "ent1_16k.bin" "ent1_4k.bin" "ent4_128k.bin" "ent4_16k.bin" "ent4_4k.bin" "ent7_128k.bin" "ent7_16k.bin" "ent7_4k.bin")
# 循环遍历文件列表
for file in "${files[@]}"; do
    echo "Processing $file"

    # 初始化时延总和
    total_lz77=0
    total_huf=0
    total_fse=0
    ratio=0

    # 执行1000次
    for i in $(seq 1 1000); do
        # 执行命令并捕获输出
        output=$(taskset -c 1 ./zstd/zstd -3 "./test_data/$file" -f 2>&1)

        # 提取每个阶段的时延
        lz77_time=$(echo "$output" | grep "ZSTD_buildSeqStore" | awk '{print $5}')
        huf_time=$(echo "$output" | grep "ZSTD_compressLiterals" | awk '{print $5}')
        fse_time=$(echo "$output" | grep "ZSTD_buildSequencesStatistics" | awk '{print $5}')
        ratio=$(echo "$output" | grep "=>" | awk '{print $3}')
        # 累加时延
        total_lz77=$((total_lz77 + lz77_time))
        total_huf=$((total_huf + huf_time))
        total_fse=$((total_fse + fse_time))
    done

    # 计算每个文件的平均时延
    avg_lz77=$((total_lz77 / 1000))
    avg_huf=$((total_huf / 1000))
    avg_fse=$((total_fse / 1000))

    # 输出每个文件的结果
    echo "Average ZSTD_buildSeqStore (LZ77) time for $file: $avg_lz77 ns"
    echo "Average ZSTD_compressLiterals (HUF) time for $file: $avg_huf ns"
    echo "Average ZSTD_buildSequencesStatistics (FSE) time for $file: $avg_fse ns"
    echo "Compression ratio for $file: $ratio"
    echo ""
done

