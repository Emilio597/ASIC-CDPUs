import os
import glob

def main():
    interval=10
    for dirpath, dirnames, filenames in os.walk("/home/user/Programs/YCSB-parallel-test/results"):
        if any(name.startswith("202") for name in dirnames):
            for dn in dirnames:
                print(f"PATH: {dirpath}/{dn}")
                thrpt_file = f"{dirpath}/{dn}/cpuutil_power_stat_run"
                with open(thrpt_file, 'r') as file:
                    lines = file.readlines()
                    last_n_lines = lines[-11:] if len(lines) >= 9 else lines

                    for line in last_n_lines:
                        print(line.strip())
                    print()
        print()
        
    
            




if __name__ == "__main__":
    main()