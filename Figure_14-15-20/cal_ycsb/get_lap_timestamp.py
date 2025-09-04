import argparse
import glob
from datetime import datetime, timedelta
import re

def get_overlap_time_range(file_list):
    """
    Calculate the common time range (overlapping range) across multiple files.
    
    Parameters:
        file_list (list): List of file paths.
        
    Returns:
        tuple: (common_start_time, common_end_time) if overlapping range exists, else None.
    """
    start_times = []
    end_times = []

    for file in file_list:
        # Read the file line by line
        with open(file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        # Extract timestamps from the file
        timestamps = []
        pattern = r'\d+ sec: (\d+) operations;'
        for line in lines:
            # if line.startswith("Run") or line.startswith("load") or line.startswith("Caught"):
            if not line.startswith("202"):
                continue  # Skip irrelevant lines
            match_res = re.search(pattern, line)
            if not match_res or match_res.group(1)=='0':
                continue
            
            parts = line.split()
            try:
                timestamps.append(f"{parts[0]} {parts[1]}")
            except IndexError:
                continue  # Skip lines that don't have timestamps

        # Get the start and end time for this file
        if timestamps:
            start_times.append(min(timestamps))
            end_times.append(max(timestamps))
            

    # Calculate the overlapping range
    common_start_time = max(start_times)
    common_end_time = min(end_times)

    if common_start_time <= common_end_time:
        return common_start_time, common_end_time
    else:
        return None
    
def get_maxrange_time_range(file_list):
    start_times = []
    end_times = []

    for file in file_list:
        # Read the file line by line
        with open(file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        # Extract timestamps from the file
        timestamps = []
        pattern = r'\d+ sec: (\d+) operations;'
        for line in lines:
            # if line.startswith("Run") or line.startswith("load") or line.startswith("Caught"):
            if not line.startswith("202"):
                continue  # Skip irrelevant lines
            match_res = re.search(pattern, line)
            if not match_res or match_res.group(1)=='0':
                continue
            
            parts = line.split()
            try:
                timestamps.append(f"{parts[0]} {parts[1]}")
            except IndexError:
                continue  # Skip lines that don't have timestamps

        # Get the start and end time for this file
        if timestamps:
            start_times.append(min(timestamps))
            end_times.append(max(timestamps))
    # Calculate the overlapping range
    maxrange_start_time = min(start_times)
    maxrange_end_time = max(end_times)
    
    if maxrange_start_time <= maxrange_end_time:
        return maxrange_start_time, maxrange_end_time
    else:
        return None


def main():
    # Parse command-line arguments
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

    # Get the common time range
    result = get_overlap_time_range(file_list)
    if result:
        # Adjust result[0] and result[1]
        start_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=10)
        end_time = datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S") - timedelta(seconds=10)
        
        # Convert adjusted times back to strings
        adjusted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        adjusted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Adjusted Common time range: {adjusted_start_time} to {adjusted_end_time}")
    else:
        print("No overlapping time range found across files.")

if __name__ == "__main__":
    main()
