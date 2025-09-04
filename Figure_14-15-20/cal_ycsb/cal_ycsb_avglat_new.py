import pandas as pd
import argparse
from get_lap_timestamp import get_overlap_time_range
import argparse
import glob
from datetime import datetime, timedelta
import re


def get_time_range_avg_lat(file_list, start_time, end_time):
    all_col_means = []
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + timedelta(seconds=0)
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - timedelta(seconds=0)
    
    for input_file in file_list:
        # Read the log data
        with open(input_file, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        filtered_lines = [line for line in lines if line.startswith("202")]
        # filtered_lines = [line for line in filtered_lines if line.split()[4]!="0"]
        #### Parse the log data into a structured format
        parsed_data = []
        pattern = r'\[(\w+):.*?Avg=(\d+\.\d+)'
        
        for line in filtered_lines:
            parts = line.split()
            timestamp = f"{parts[0]} {parts[1]}"
            try:
                matches = re.findall(pattern, line)
    
                line_info_dict={}
                line_info_dict["timestamp"] = timestamp
                for m_info in matches:
                    line_info_dict[m_info[0]] = float(m_info[1])
                parsed_data.append(line_info_dict)
            except (ValueError, IndexError):
                continue  # Skip lines that do not match the expected format
            
        # Convert to DataFrame
        df = pd.DataFrame(parsed_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        
        # 5. 过滤出指定时间区间内的数据
        filtered_data = df.loc[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)].copy()
        filtered_data.drop(columns=["timestamp"], errors="ignore", inplace=True)
        if filtered_data.empty:
            continue
        
        # 对剩余数值列求平均
        col_means = filtered_data.mean()  # 返回一个 Series
        all_col_means.append(col_means)
        # print("filtered_data", filtered_data)
        # print("col_means", col_means)
    df_all_means = pd.DataFrame(all_col_means)
    # print("df_all_means", df_all_means)
    final_mean = df_all_means.mean(axis=0)
    return final_mean
    


def main():
    parser = argparse.ArgumentParser(description="Extract log data within a specified time range.")
    parser.add_argument("--input_file_pattern", required=True, help="Path to the input log file.")
    parser.add_argument("--start_time", required=True, help="Start time in format 'YYYY-MM-DD HH:MM:SS'.")
    parser.add_argument("--end_time", required=True, help="End time in format 'YYYY-MM-DD HH:MM:SS'.")
    args = parser.parse_args()
    
    file_list = glob.glob(args.input_file_pattern)

    if not file_list:
        print("PARSE FILE:No files found matching the pattern.")
        return

    # Call the extract_data function with parsed arguments
    final_mean = get_time_range_avg_lat(file_list, args.start_time, args.end_time)
    print(final_mean)


if __name__ == "__main__":
    main()