import os
import csv

# prompt the user for the directory path containing the .csv files to be searched
csv_dir = input('Enter the path to the directory containing the CSV files to be searched: ')

# prompt the user for the path to the reference CSV file
ref_path = input('Enter the path to the reference CSV file containing the search strings: ')

# prompt the user for the path to the output CSV file
output_path = input('Enter the path to the output CSV file: ')

# read the search strings from the reference CSV file
with open(ref_path, 'r') as ref_file:
    reader = csv.reader(ref_file)
    search_strings = [row[0] for row in reader]

# list all .csv files in the specified directory
csv_files = [os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.endswith('.csv')]

# create the output CSV file and write the headers
with open(output_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    headers = ['file']
    headers.extend(search_strings)
    writer.writerow(headers)

    # loop through each .csv file and check for the presence of each search string
    for f in csv_files:
        row = [os.path.basename(f)]
        with open(f, 'r') as csv_file:
            counts = [0] * len(search_strings)
            for line in csv_file:
                for i, search_str in enumerate(search_strings):
                    if search_str in line:
                        counts[i] = 1  # Update this line to set presence as '1'
            row.extend(counts)
        writer.writerow(row)
