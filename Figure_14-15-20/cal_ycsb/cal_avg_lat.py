import pandas as pd
import argparse
from get_lap_timestamp import get_overlap_time_range
import argparse
import glob
from datetime import datetime, timedelta
import re

# def extract_data(input_file, start_time, end_time):
#     """
#     Extracts log data within the specified time range, ignoring irrelevant lines, and writes to a new file.
    
#     Parameters:
#         input_file (str): Path to the input log file.
#         # output_file (str): Path to save the filtered log data.
#         start_time (str): Start time in the format 'YYYY-MM-DD HH:MM:SS'.
#         end_time (str): End time in the format 'YYYY-MM-DD HH:MM:SS'.
#     """
#     # Read the log data
#     with open(input_file, 'r') as file:
#         lines = [line.strip() for line in file if line.strip()]
    
#     # Parse the log data into a structured format
#     parsed_data = []
#     pattern = r'\[(\w+):.*?Avg=(\d+\.\d+)'
    
#     for line in lines:
#         # if line.startswith("Run runtime") or line.startswith("Run operations") or line.startswith("Run throughput"):
#         if not line.startswith("202"):
#             continue  # Skip irrelevant lines
#         parts = line.split()
#         timestamp = f"{parts[0]} {parts[1]}"
#         try:
#             matches = re.findall(pattern, line)
 
#             line_info_dict={}
#             line_info_dict["timestamp"] = timestamp
#             for m_info in matches:
#                 line_info_dict[m_info[0]] = float(m_info[1])
#             parsed_data.append(line_info_dict)
#         except (ValueError, IndexError):
#             continue  # Skip lines that do not match the expected format
        
#     # Convert to DataFrame
#     df = pd.DataFrame(parsed_data)
    
#     # Filter data based on time range
#     filtered_data = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
#     filtered_data = filtered_data.drop(columns=["timestamp"])
#     # print("BBBB", filtered_data)
#     return filtered_data.mean()


# def main():
#     # Parse command-line arguments
#     parser = argparse.ArgumentParser(description="Extract log data within a specified time range.")
#     parser.add_argument("--input_file_pattern", required=True, help="Path to the input log file.")
#     args = parser.parse_args()
    
#     file_list = glob.glob(args.input_file_pattern)

#     if not file_list:
#         print("PARSE FILE:No files found matching the pattern.")
#         return

#     # Get the common time range
#     result = get_overlap_time_range(file_list)
#     if result:
#         # Adjust result[0] and result[1]
#         start_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=0)
#         end_time = datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S") - timedelta(seconds=0)
        
#         # Convert adjusted times back to strings
#         adjusted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
#         adjusted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        
#         print(f"\n\nAdjusted Common time range: {adjusted_start_time} to {adjusted_end_time}")
#     else:
#         print("No overlapping time range found across files.")
    
#     # Call the extract_data function with parsed arguments
#     total_series = pd.Series(dtype=float)
#     for f in file_list:
#         f_mean_series = extract_data(f, adjusted_start_time, adjusted_end_time)
#         total_series = total_series.add(f_mean_series, fill_value=0)
#         print(f"The latency of file {f} is: ", f_mean_series)
#     total_series_avg = total_series/len(file_list)
#     print("\n\nTotal total_series_avg is: ", total_series_avg)












def extract_data(input_file):
    # Read the log data
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    filtered_lines = [line for line in lines if line.startswith("202")]
    filtered_lines = [line for line in filtered_lines if line.split()[4]!="0"][-20:]
    # Parse the log data into a structured format
    parsed_data = []
    pattern = r'\[(\w+):.*?Avg=(\d+\.\d+)'
    
    for line in filtered_lines:
        parts = line.split()
        # timestamp = f"{parts[0]} {parts[1]}"
        try:
            matches = re.findall(pattern, line)
 
            line_info_dict={}
            # line_info_dict["timestamp"] = timestamp
            for m_info in matches:
                line_info_dict[m_info[0]] = float(m_info[1])
            parsed_data.append(line_info_dict)
        except (ValueError, IndexError):
            continue  # Skip lines that do not match the expected format
        
    # Convert to DataFrame
    df = pd.DataFrame(parsed_data)
    
    return df.mean()


def main():
    parser = argparse.ArgumentParser(description="Extract log data within a specified time range.")
    parser.add_argument("--input_file_pattern", required=True, help="Path to the input log file.")
    args = parser.parse_args()
    
    file_list = glob.glob(args.input_file_pattern)

    if not file_list:
        print("PARSE FILE:No files found matching the pattern.")
        return
    
    # Call the extract_data function with parsed arguments
    total_series = pd.Series(dtype=float)
    for f in file_list:
        f_mean_series = extract_data(f)
        total_series = total_series.add(f_mean_series, fill_value=0)
        print(f"The latency of file {f} is: ", f_mean_series)
    total_series_avg = total_series/len(file_list)
    print("\n\nTotal total_series_avg is: ", total_series_avg)


if __name__ == "__main__":
    main()