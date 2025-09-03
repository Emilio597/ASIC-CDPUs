from get_lap_timestamp import get_maxrange_time_range, get_overlap_time_range
import argparse
import glob
from datetime import datetime, timedelta
import re


def get_time_range_total_thrpt(file_list, start_time_str, end_time_str):
    all_proc_throuput = 0
    
    s_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    e_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
    time_interval = max(0, (e_time - s_time).total_seconds())
    if not time_interval:
        return False
    for file in file_list:
        # Read the file line by line
        with open(file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        # pattern = r'\d+ sec: (\d+) operations;'
        start_time_throuput = 0
        end_time_throuput = 0
        for line in lines:
            # if line.startswith("Run") or line.startswith("load") or line.startswith("Caught"):
            if not line.startswith("202"):
                continue  # Skip irrelevant lines
            # match_res = re.search(pattern, line)
            # if not match_res or match_res.group(1)=='0':
            #     continue
            
            parts = line.split()
            # print("PARTS:", parts[0], parts[1], parts[2], parts[3], parts[4])
            c_time = datetime.strptime(parts[0]+' '+parts[1], "%Y-%m-%d %H:%M:%S")


            if c_time == s_time:
                start_time_throuput = int(parts[4])
            if c_time == e_time:
                end_time_throuput = int(parts[4])
        if start_time_throuput > end_time_throuput:
            end_time_throuput = int(parts[4])
        file_total_throughput = end_time_throuput - start_time_throuput
                
        # print(f"{file}", file_total_throughput/time_interval)

        file_avg_throuput = file_total_throughput / time_interval
        all_proc_throuput += file_avg_throuput
    return all_proc_throuput


def slice_time_range(start_time_str, end_time_str, time_delta):
    # 转换为 datetime 对象
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

    # 时间间隔
    time_d = timedelta(seconds=time_delta)

    # 生成时间戳范围
    time_ranges = []
    current_start = start_time
    while current_start + time_d <= end_time:
        current_end = current_start + time_d
        time_ranges.append((current_start.strftime('%Y-%m-%d %H:%M:%S'), current_end.strftime('%Y-%m-%d %H:%M:%S')))
        current_start = current_end

    # 输出结果
    return time_ranges



def main():
    parser = argparse.ArgumentParser(description="Find common time range across multiple files.")
    parser.add_argument(
        "--input_file_pattern", required=True, help="Glob pattern to match the log files (e.g., 'logs/*.txt')."
    )
    args = parser.parse_args()

    # Collect files based on the pattern
    file_list = glob.glob(args.input_file_pattern)

    if not file_list:
        print("TIME_LAP:No files found matching the pattern.")
        return

    # # Get the common time range
    start_time_str, end_time_str = get_maxrange_time_range(file_list)
    time_delta = 5
    time_ranges = slice_time_range(start_time_str, end_time_str, time_delta)
    time_interval_throughput_list = []
    for tr in time_ranges:
        res = get_time_range_total_thrpt(file_list, tr[0], tr[1])
        time_interval_throughput_list.append(res)
        print("Time Interval:", tr)
        print("Interval Total Throuput:", res)
        print("")
        
    print(f"Max {time_delta}s Interval total Throuput: ", max(time_interval_throughput_list))

    
        
if __name__ == "__main__":
    main()