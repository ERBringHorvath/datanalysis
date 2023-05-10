from Bio import SeqIO
import csv
from collections import defaultdict

# File path
genbank_path = '/Users/ebh/Desktop/AphSulDistro/amsul.gb'

# Read the GenBank file
records = list(SeqIO.parse(genbank_path, 'genbank'))

# A list to hold the extracted data
data = []

# Loop over the records
for record in records:
    for feature in record.features:
        if feature.type == 'source':
            organism = feature.qualifiers.get('organism', ['Unknown'])[0]
            country = feature.qualifiers.get('country', ['Unknown'])[0]
            isolation_source = feature.qualifiers.get('isolation_source', ['Unknown'])[0]
            data.append([organism, country, isolation_source])

# Save the data to a CSV file
with open('output1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Organism', 'Country', 'Isolation Source'])
    writer.writerows(data)

# Count unique instances
counts = defaultdict(lambda: defaultdict(int))

for organism, country, isolation_source in data:
    counts['Organism'][organism] += 1
    counts['Country'][country] += 1
    counts['Isolation Source'][isolation_source] += 1

# Save the counts to a CSV file
with open('output2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Category', 'Value', 'Count'])

    for category in counts:
        for value in counts[category]:
            writer.writerow([category, value, counts[category][value]])

