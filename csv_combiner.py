import os
import glob
import pandas as pd

# prompt user for the directory path
path = input("Enter the directory path where your csv files are stored: ")

# prompt user for the desired name of the combined file
filename = input("Enter the desired name of the combined file: ")

# set working directory
os.chdir(path)

# get all csv files in the directory
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# initialize an empty list to store valid csv files
valid_filenames = []

# iterate through all csv files and check if they are non-empty and have a header row
for f in all_filenames:
    try:
        df = pd.read_csv(f)
        if not df.empty and list(df.columns) != []:
            valid_filenames.append(f)
        else:
            print(f"Skipping file {f} because it is empty or has no header row.")
    except:
        print(f"Skipping file {f} due to an error while reading.")

# combine all valid csv files into one dataframe
combined_csv = pd.concat([pd.read_csv(f) for f in valid_filenames ])

# write the combined dataframe to a csv file
combined_csv.to_csv(filename + ".csv", index=False, encoding='utf-8-sig')

print("Combined csv file has been created and stored in the same directory as " + filename + ".csv!")
