import os
from cal_ycsb_thrpt_new import get_time_range_total_thrpt, slice_time_range
from get_lap_timestamp import get_maxrange_time_range
import glob
from cal_ycsb_avglat_new import get_time_range_avg_lat

def main():
    time_delta = 10
    for dirpath, dirnames, filenames in os.walk("/home/user/Programs/YCSB-parallel-test/results"):
        if "run" in dirnames:
            file_path_patten = f"{dirpath}/run/ycsb*"
            # print(file_path_patten)
            file_list = glob.glob(file_path_patten)

            if not file_list:
                print("TIME_LAP:No files found matching the pattern.")
                return

            # Get the common time range
            start_time_str, end_time_str = get_maxrange_time_range(file_list)
            
            time_ranges = slice_time_range(start_time_str, end_time_str, time_delta)
            time_interval_throughput_list = []
            
            print(f"{dirpath}")
            with open(f"{dirpath}/new_total_run_throuput_{time_delta}s", "w") as f:
                for tr in time_ranges:
                    res = get_time_range_total_thrpt(file_list, tr[0], tr[1])
                    time_interval_throughput_list.append((res, tr))
                    f.write(f"Time Interval: {tr}\n")
                    f.write(f"Each Interval Total Throuput: {res}\n\n")
                max_tuple = max(time_interval_throughput_list, key=lambda x: x[0])
                max_val, max_tr = max_tuple
                
                f.write(f"The Max Troughput Interval({time_delta}s): {max_val}")
                f.write(f"The Max Troughput Time RANGE: {max_tr[0]} {max_tr[1]}")
            with open(f"{dirpath}/new_total_run_avg_lat_{time_delta}s", "w") as f2:
                lat_mean_series = get_time_range_avg_lat(file_list, max_tr[0], max_tr[1])
                output_str = "  ".join(f"{col}={val:.2f}" for col, val in lat_mean_series.items())
                f2.write(output_str)
    
            

if __name__ == "__main__":
    main()