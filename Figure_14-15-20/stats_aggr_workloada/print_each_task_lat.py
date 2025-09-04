import os
import glob
import re

def main():
    interval=10
    for dirpath, dirnames, filenames in os.walk("/home/user/Programs/YCSB-parallel-test/results"):
        if any(name.startswith("202") for name in dirnames):
            for dn in dirnames:
                print(f"PATH: {dirpath}/{dn}", end="\t")
                thrpt_file = f"{dirpath}/{dn}/new_total_run_avg_lat_{interval}s"
                with open(thrpt_file, 'r') as file:
                    lines = file.readlines()
                    last_five_lines = lines[-5:] if len(lines) >= 5 else lines

                    for line in last_five_lines:
                        line = re.sub(r'\s+', ' ', line).strip()
                        print(line, end=" ")
                    print()  

        print()
        
    
            




if __name__ == "__main__":
    main()