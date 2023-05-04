import os
import subprocess

# Prompt user for directory path
db_dir = input("Enter path to directory containing blast+ nucleotide databases: ")
if not os.path.isdir(db_dir):
    print("Invalid directory path")
    exit()

# Prompt user for FASTA query file path
query_path = input("Enter path to nucleotide FASTA query: ")
if not os.path.isfile(query_path):
    print("Invalid FASTA query path")
    exit()

# Prompt user for output directory path
output_dir = input("Enter path to output directory: ")
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

# Iterate over all databases in directory
for file_name in os.listdir(db_dir):
    if file_name.endswith(".nhr"):
        # Build file paths
        db_name = os.path.splitext(file_name)[0]
        db_path = os.path.join(db_dir, db_name)
        output_file = os.path.join(output_dir, f"{db_name}_results.txt")

        # Run BLAST query and save results
        cmd = f"blastn -query {query_path} -db {db_path} -out {output_file}"
        subprocess.run(cmd, shell=True)

print("All BLAST queries complete.")

