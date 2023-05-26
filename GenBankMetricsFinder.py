from Bio import SeqIO
import csv
from collections import defaultdict
import os
import concurrent.futures

def process_file(file):
    # Create a list to hold the extracted data
    data = []

    # Check if the file is a GenBank file
    if file.endswith('.gbk'):  
        # Read the GenBank file
        records = list(SeqIO.parse(genbank_dir + file, 'genbank'))

        # Loop over the records
        for record in records:
            for feature in record.features:
                if feature.type == 'source':
                    organism = feature.qualifiers.get('organism', ['Unknown'])[0]
                    country = feature.qualifiers.get('country', ['Unknown'])[0]
                    isolation_source = feature.qualifiers.get('isolation_source', ['Unknown'])[0]
                    host = feature.qualifiers.get('host', ['Unknown'])[0]  # Extract the HOST information
                    version = record.annotations.get('accessions', ['Unknown'])[0]  # Extract the VERSION information
                    data.append([organism, country, isolation_source, host, version])

    return data  # Always return data, which may be an empty list if the file was not a '.gbk' file

# Directory path
genbank_dir = '/Path/to/files/'

# Get the list of files in the directory
files = os.listdir(genbank_dir)

# Number of threads to use (default is 3, change as needed)
num_threads = 3

# Process the files in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = executor.map(process_file, files)

# Gather all the data
data = []
for result in results:
    data.extend(result)

# Save the data to a CSV file
with open('Metrics.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Organism', 'Country', 'Isolation Source', 'Host', 'Version'])
    writer.writerows(data)

# Count unique instances for summed data
counts = defaultdict(lambda: defaultdict(int))

for organism, country, isolation_source, host, version in data:
    counts['Organism'][organism] += 1
    counts['Country'][country] += 1
    counts['Isolation Source'][isolation_source] += 1
    counts['Host'][host] += 1

# Save the summed data to a CSV file
with open('MetricsSummed.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Category', 'Value', 'Count'])

    for category in counts:
        for value in counts[category]:
            writer.writerow([category, value, counts[category][value]])

