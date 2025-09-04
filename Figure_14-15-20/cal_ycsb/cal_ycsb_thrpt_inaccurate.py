import pandas as pd
import argparse
from get_lap_timestamp import get_overlap_time_range
import argparse
import glob
from datetime import datetime, timedelta

def extract_data(input_file, start_time, end_time):
    """
    Extracts log data within the specified time range, ignoring irrelevant lines, and writes to a new file.
    
    Parameters:
        input_file (str): Path to the input log file.
        # output_file (str): Path to save the filtered log data.
        start_time (str): Start time in the format 'YYYY-MM-DD HH:MM:SS'.
        end_time (str): End time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    # Read the log data
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    # Parse the log data into a structured format
    parsed_data = []
    for line in lines:
        # if line.startswith("Run runtime") or line.startswith("Run operations") or line.startswith("Run throughput"):
        if not line.startswith("202"):
            continue  # Skip irrelevant lines
        parts = line.split()
        timestamp = f"{parts[0]} {parts[1]}"
        try:
            sec = int(parts[2])
            operations = int(parts[4])
            parsed_data.append({"timestamp": timestamp, "sec": sec, "operations": operations})
        except (ValueError, IndexError):
            continue  # Skip lines that do not match the expected format
    
    # Convert to DataFrame
    df = pd.DataFrame(parsed_data)
    
    # Filter data based on time range
    filtered_data = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
    
    # Save the filtered data to the output file
    # filtered_data.to_csv(output_file, index=False,)
    # print(f"Filtered data saved to {output_file}")
    
    if not filtered_data.empty:
        operations_diff = filtered_data["operations"].iloc[-1] - filtered_data["operations"].iloc[0]
        sec_diff = filtered_data["sec"].iloc[-1] - filtered_data["sec"].iloc[0] 
        average_operations = operations_diff / sec_diff
        
        return average_operations
    else:
        raise ValueError(f"No data found between {start_time} and {end_time}.")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract log data within a specified time range.")
    parser.add_argument("--input_file_pattern", required=True, help="Path to the input log file.")
    # parser.add_argument("--output_file", required=True, help="Path to save the filtered log data.")
    # parser.add_argument("--start_time", required=True, help="Start time in format 'YYYY-MM-DD HH:MM:SS'.")
    # parser.add_argument("--end_time", required=True, help="End time in format 'YYYY-MM-DD HH:MM:SS'.")
    args = parser.parse_args()
    
    file_list = glob.glob(args.input_file_pattern)

    if not file_list:
        print("PARSE FILE:No files found matching the pattern.")
        return
    
    # Get the common time range
    result = get_overlap_time_range(file_list)
    if result:
        # Adjust result[0] and result[1]
        start_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=0)
        end_time = datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S") - timedelta(seconds=0)
        
        # Convert adjusted times back to strings
        adjusted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        adjusted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Adjusted Common time range: {adjusted_start_time} to {adjusted_end_time}")
    else:
        print("No overlapping time range found across files.")
    
    # Call the extract_data function with parsed arguments
    total_throughput=0
    for f in file_list:
        average_operations = extract_data(f, adjusted_start_time, adjusted_end_time)
        print(f"Average operations of file {f}: {average_operations}")
        total_throughput += average_operations
        
    print("\n\nTotal Throughput is : {:.2f}".format(total_throughput))

if __name__ == "__main__":
    main()