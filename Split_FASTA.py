from Bio import SeqIO
from tqdm import tqdm

# Prompt the user for the input file
input_file = input("Enter the input file: ")

# Prompt the user for the output directory
output_dir = input("Enter the output directory: ")

# Count the total number of records in the input file
total_records = sum(1 for record in SeqIO.parse(input_file, "fasta"))

# Loop through each record in the input file and write it to a separate output file, with a progress bar
with tqdm(total=total_records, desc="Processing") as pbar:
    for record in SeqIO.parse(input_file, "fasta"):
        # Replace "output_dir" with the output directory provided by the user, and use the record ID as the filename
        output_file = f"{output_dir}/{record.id}.fasta"
        SeqIO.write(record, output_file, "fasta")
        pbar.update(1)

