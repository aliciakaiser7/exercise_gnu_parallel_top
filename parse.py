import argparse
import time
import os
import datetime 

# Argument parser setup
parser = argparse.ArgumentParser(
    prog="tailf",
    description="Reads and prints the last 10 lines of a file line by line every 10 seconds",
)
parser.add_argument("logfile", nargs="?", help="Path to the log file")
args = parser.parse_args()


# Function to clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
    columns = input_line.strip().split(',')
    column_names = [f'column_{i+1}' for i in range(len(columns))]
    return dict(zip(column_names, columns))

# Continuously read and print the last 10 lines of the file every 10 seconds
while True:
    with open(args.logfile, "r", encoding="utf-16") as file:
        lines = file.readlines()
        # Display only the last 10 lines
        last_10_lines = lines[-10:]

    # Clear the console
    clear_console()

    def parse(input_line: str) -> dict:
    columns = input_line.strip().split(',')
    column_names = [f'column_{i+1}' for i in range(len(columns))]
    parsed_dict = dict(zip(column_names, columns))
   
    # Print each line
    #for line in last_10_lines:
        #print(line.replace("\x00", ""), end="")


    # Print each line based on the parsed dictionary  
    for line in last_10_lines:
        parsed_line = parse(line)
        formatted_line = ", ".join(f"{key}: {value}" for key, value in parsed_line.items())
        print(formatted_line)


    # Wait for 10 seconds
    time.sleep(10)

