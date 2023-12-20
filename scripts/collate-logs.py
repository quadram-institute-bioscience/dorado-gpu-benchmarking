import os
import csv
import argparse
from datetime import datetime
import re

def parse_log_file(file_path):
    with open(file_path, 'r') as file:
        basecalled_value = None
        model_memory_value = None
        decode_memory_value = None
        elapsed_time = None
        start_time = None
        end_time = None

        for line in file:
            # Extract timestamp
            timestamp_match = re.search(r'\[(.*?)\]', line)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                if start_time is None:
                    start_time = timestamp
                end_time = timestamp

            # Extract other values
            if 'Basecalled @ Samples/s' in line and basecalled_value is None:
                basecalled_value = float(re.findall(r'[\d\.]+e[+-]\d+', line)[0])
            elif 'Model memory' in line and model_memory_value is None:
                model_memory_value = float(re.findall(r'\d+\.\d+', line)[0])
            elif 'Decode memory' in line and decode_memory_value is None:
                decode_memory_value = float(re.findall(r'\d+\.\d+', line)[0])

        if start_time and end_time:
            elapsed_time = end_time - start_time

        return basecalled_value, model_memory_value, decode_memory_value, elapsed_time

def process_log_files(directory, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Basecalled', 'Model Memory', 'Decode Memory', 'Elapsed Time'])

        for filename in os.listdir(directory):
            if filename.endswith('.log'):
                file_path = os.path.join(directory, filename)
                basecalled, model_memory, decode_memory, elapsed_time = parse_log_file(file_path)
                csvwriter.writerow([filename, basecalled, model_memory, decode_memory, elapsed_time])

def main():
    parser = argparse.ArgumentParser(description='Process log files and output to a CSV file.')
    parser.add_argument('directory', type=str, help='Directory containing log files')
    parser.add_argument('output_csv', type=str, help='Output CSV file path')

    args = parser.parse_args()

    process_log_files(args.directory, args.output_csv)

if __name__ == "__main__":
    main()
