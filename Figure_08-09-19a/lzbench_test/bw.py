import re

def calculate_bandwidth(file_name):
    # 打开并读取文件
    with open(file_name, 'r') as file:
        content = file.read()

    # 使用正则表达式匹配每行中的压缩和解压带宽
    # pattern = r'([\d.]+)\s*MB/s\s+(\d+)\s*MB/s'
    pattern = r'([\d.]+)\s*MB/s\s+([\d.]+)\s*MB/s'

    lines = content.splitlines()

    # 初始化压缩和解压带宽总和
    total_compress_bandwidth = 0
    total_decompress_bandwidth = 0

    # 逐行分析
    for line in lines:
        # 只处理包含 "zstd" 的行
        if "snappy 1.1.10" in line or "zstd 1.5.5 -1" in line or "zlib 1.2.11 -1" in line:
            match = re.search(pattern, line)

            if match:
                print(line)
                compress_bandwidth = float(match[1])
                decompress_bandwidth = float(match[2])
                total_compress_bandwidth += compress_bandwidth
                total_decompress_bandwidth += decompress_bandwidth

    # 输出结果
    print(f"Total compress bandwidth: {total_compress_bandwidth} MB/s")
    print(f"Total decompress bandwidth: {total_decompress_bandwidth} MB/s")
    print(f"Total combined bandwidth (compress + decompress): {total_compress_bandwidth + total_decompress_bandwidth} MB/s")

# 输入文件名并调用函数
file_name = "output_lzbench.log"
calculate_bandwidth(file_name)
