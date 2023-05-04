import subprocess
import os

input_dir = input("Enter the directory containing the input genome fasta files: ")
output_dir = input("Enter the output directory for the blast databases: ")

if not os.path.exists(output_dir):
	os.makedirs(output_dir)

extensions = [".fasta", ".faa", ".fa", ".fna", ".fas"]

for filename in os.listdir(input_dir):
	if any(filename.endswith(ext) for ext in extensions):
		input_file = os.path.join(input_dir, filename)
		base_name = os.path.splitext(filename)[0]
		output_file = os.path.join(output_dir, base_name)
		
		cmd = "makeblastdb -in " + input_file + " -out " + output_file + " -dbtype nucl"
		subprocess.call(cmd, shell=True)
