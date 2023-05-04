import os
import io
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline

def is_fasta_file(filename):
    fasta_extensions = ['.fasta', '.fna', '.ffn', '.faa', '.frn', '.fa']
    _, ext = os.path.splitext(filename)
    return ext.lower() in fasta_extensions

# Change this to wherever your files are
reference_gene_fasta = 'FILE'
genomes_directory = 'PATH'
blast_dbs_directory = 'PATH'
output_file = '5_prime_UTR.fasta'

# Search for reference gene in each genome and save the 5-prime UTR
utr_records = []
for genome_file in os.listdir(genomes_directory):
    if is_fasta_file(genome_file):
        genome_path = os.path.join(genomes_directory, genome_file)
        genome_name = os.path.splitext(genome_file)[0]
        blast_db_path = os.path.join(blast_dbs_directory, genome_name)
        
        print(f"Processing {genome_file}")

        # Perform local BLAST search
        blastn_cline = NcbiblastnCommandline(query=reference_gene_fasta,
                                             db=blast_db_path,
                                             outfmt=5)
        stdout, stderr = blastn_cline()
        blast_record = NCBIXML.read(io.StringIO(stdout))

        # Find the best hit
        if len(blast_record.alignments) > 0:
            alignment = blast_record.alignments[0]
            hsp = alignment.hsps[0]

            print(f"Best hit for {genome_file}: {alignment.hit_id}, Score: {hsp.score}")

            # Extract 5-prime UTR
            utr_start = hsp.sbjct_start - 200 if hsp.sbjct_start > 200 else 0
            utr_end = hsp.sbjct_start

            # Get the contig with the matching hit
            contig_id = alignment.hit_def.split()[0]  # Extract the contig ID from the hit_def attribute
            print(f"Contig ID: {contig_id}")
            contig = None
            with open(genome_path, 'r') as genome_f:
                for seq_record in SeqIO.parse(genome_f, 'fasta'):
                    if seq_record.id == contig_id:
                        contig = seq_record
                        break

            if contig:
                print(f"Contig found: {contig.id}")
                if hsp.strand[1] == -1:  # Antisense strand
                    utr_seq = contig.seq.reverse_complement()[utr_start:utr_end]
                else:  # Sense strand
                    utr_seq = contig.seq[utr_start:utr_end]

                best_utr = SeqRecord(utr_seq, id=contig.id, description=f'5-prime UTR of {contig.description}')

                if best_utr:
                    print(f"5-prime UTR generated: {best_utr.id}")
                    utr_records.append(best_utr)

# Write 5-prime UTRs to a new multi-FASTA file
print(f"Writing {len(utr_records)} 5-prime UTRs to {output_file}")
with open(output_file, 'w') as output_f:
    SeqIO.write(utr_records, output_f, 'fasta')


