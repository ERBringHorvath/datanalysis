import pandas as pd
from Bio import SeqIO

# read the CSV file into a pandas DataFrame
df = pd.read_csv('file.csv')

# remove the ">" character from each header and convert the column of headers to a set for faster access
headers = set(df['headers'].str.lstrip('>'))  # replace 'header_column' with the name of your header column

# read the multi-FASTA file
fasta_sequences = SeqIO.parse(open('multi-FASTA.fa'),'fasta')

# open a new multi-FASTA file to write the matched sequences
with open('output.fasta', 'w') as out_file:
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        if name in headers:
            # write the fasta record to the new file
            SeqIO.write(fasta, out_file, 'fasta')
