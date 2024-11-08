import time
import os
import argparse
parser = argparse.ArgumentParser(
    prog="tailf",
    description="Reads and prints the last 10 lines of a file line by line every 10 seconds",
)
parser.add_argument("logfile", help="Path to the log file")
parser.add_argument(
    "--total-jobs", "-tj", dest="tj", type=int, help="The number of jobs in the order"
)
args = parser.parse_args()
tj = args.tj
def failed_red(failed_count):
    if failed_count > 0:
        return f"\033[31m{failed_count}\033[0m"
    return f"{failed_count}"
def clear_console():
    print("\033[H\033[J", end="")
def parse(input_line: str) -> dict:
    columns = input_line.split()
    parsed = {
        "seq": int(columns[0]),
        "host": columns[1],
        "starttime": time.gmtime(float(columns[2])),
        "jobRuntime": float(columns[3]),
        "send": int(columns[4]),
        "receive": int(columns[5]),
        "exitval": int(columns[6]),
        "signal": int(columns[7]),
        "command": " ".join(columns[8:]),
    }
    return parsed
def progress(lines, total_jops):
    return (len(lines) / tj) * 100 if tj else 0
def ascii_progress_bar(percentage, bar_length=50):
    if percentage < 33:
        color = "\033[31m"
    elif percentage < 66:
        color = "\033[33m"
    else: 
        color = "\033[32m"
    filled_length = int(bar_length * percentage // 100)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    return f"{color}[{bar}] {percentage:.2f}%\033[0m"
try:
    with open(args.logfile, "r") as file:
        lines = []
        hosts = {}
        file.readline()
        while True:
            new_lines = file.readlines()
            if new_lines:
                lines.extend(new_lines)
            clear_console()
            print(ascii_progress_bar(progress(lines,tj)))
            print("--------------------------------------------------------------")
            print("Host         Throughput (jobs/s)    Total   Successful  Failed")
            print("--------------------------------------------------------------")
            for line in new_lines:
                parsed_line = parse(line.replace("\x00", ""))
                host = parsed_line["host"]
                if host not in hosts:
                    hosts[host] = {
                        "jobs": [],
                        "total": 0,
                        "successful": 0,
                        "failed": 0,
                    }
                hosts[host]["jobs"].append(parsed_line)
                hosts[host]["total"] += 1
                if parsed_line["exitval"] == 0:
                    hosts[host]["successful"] += 1
                else:
                    hosts[host]["failed"] += 1
            throughput_overall = 0
            totel_overall = 0
            succsessful_overall = 0
            failed_overall = 0
            for host, stats in hosts.items():
                throughput = len(stats["jobs"]) / (time.mktime(time.localtime()) - time.mktime(stats["jobs"][0]["starttime"]))
                throughput_overall += throughput
                totel_overall += stats["total"]
                succsessful_overall += stats["successful"]
                failed_overall += stats["failed"]
                print(
    f"{host:12} {throughput:.2f}                  {stats['total']:5}    {stats['successful']:5}        {failed_red(stats['failed']):5}"
)
                print(
    f"{'overall':12} {throughput_overall:.2f}                  {totel_overall:5}    {succsessful_overall:5}        {failed_red(failed_overall):5}"
)

            print("--------------------------------------------------------------")
            print(
                f"{'overall':12} {throughput_overall:.2f}                  {totel_overall:5}    {succsessful_overall:5}        {failed_overall:5}"
            )
            
            if progress(lines,tj) == 100:
                break
            time.sleep(1)
except FileNotFoundError:
    print(f"Error: The file '{args.logfile}' was not found.")
except IOError as e:
    print(f"Error reading the file '{args.logfile}': {e}")
except ZeroDivisionError:
    print("Error: Total jobs parameter must be a positive integer.")