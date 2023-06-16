import os

# specify the directory you want to start from
rootDir = ''
char_limit = 3500  # change the limit as per your requirements

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if fname.endswith('.fasta'):
            file_path = os.path.join(dirName, fname)
            with open(file_path, 'r') as file:
                file_content = file.readlines()

            character_count = sum(len(line.strip()) for line in file_content if not line.startswith('>'))
            if character_count < char_limit:
                os.remove(file_path)
                print(f"File {file_path} has been deleted.")

# count remaining fasta files
remaining_files = sum(1 for dirName, subdirList, fileList in os.walk(rootDir) for fname in fileList if fname.endswith('.fasta'))
print(f"Remaining FASTA files in directory: {remaining_files}")

