import sys

def parse_iolog(file_path, chunk):
    read_addresses = set()
    duplicate_addresses = set()
    count = 0
    output_file = f"{file_path.rsplit('.', 1)[0]}_fix.txt"
    
    try:
        with open(file_path, 'r') as file, open(output_file, 'w') as output:
            for line in file:
                parts = line.split()

                if len(parts) >= 5 and parts[2] == "read":
                    address = int(int(parts[3]) / chunk)
                    
                    if address in read_addresses:
                        count += 1
                        duplicate_addresses.add(address)
                    else:
                        read_addresses.add(address)
                        output.write(line)  # Write to output file if no duplicate address
                else:
                    output.write(line)  # Write line if it doesn't meet the "read" condition

        if duplicate_addresses:
            print(f"duplen: {len(duplicate_addresses)}, total count: {count}")
        else:
            print("No duplicate read addresses found.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <iolog_file> <chunk>k")
        sys.exit(1)
    iolog_file = sys.argv[1]
    chunk=int(sys.argv[2]) * 1024
    print(f"Chunk size: {chunk}")
    parse_iolog(iolog_file, chunk)
