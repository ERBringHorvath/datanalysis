import os
from Bio import SeqIO
from tqdm import tqdm

def split_genbank_file(input_filename, output_dir):
    records = list(SeqIO.parse(input_filename, "genbank"))
    filename_counters = {}

    for i, record in tqdm(enumerate(records), total=len(records), desc="Splitting Genbank File"):
        version = record.annotations['accessions'][0] if 'accessions' in record.annotations and record.annotations['accessions'] else f"record_{i+1}"
        
        # Ensure unique filename
        if version in filename_counters:
            filename_counters[version] += 1
            version = f"{version}_{filename_counters[version]}"
        else:
            filename_counters[version] = 0
        
        output_filename = os.path.join(output_dir, f"{version}.gbk")
        with open(output_filename, "w") as output_handle:
            SeqIO.write(record, output_handle, "genbank")

# Usage
input_file = input("Please enter the path of your multi-genbank file: ")
output_dir = input("Please enter the target directory for output files: ")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

split_genbank_file(input_file, output_dir)
