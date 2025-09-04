import os
import glob

def main():
    interval=10
    for dirpath, dirnames, filenames in os.walk("/home/user/Programs/YCSB-parallel-test/results"):
        if any(name.startswith("202") for name in dirnames):
            for dn in dirnames:
                print(f"PATH: {dirpath}/{dn}", end="\t")
                thrpt_file = f"{dirpath}/{dn}/new_total_run_throuput_{interval}s"
                with open(thrpt_file, 'r') as file:
                    for line in file:
                        if line.startswith("The Max Troughput Interval"):
                            max_throughput = line.split("The Max Troughput Time RANGE:")[0].strip()
                            corres_interval = line.split("The Max Troughput Time RANGE:")[1].strip()
                            print(max_throughput, corres_interval)
        print()
        
    
            




if __name__ == "__main__":
    main()