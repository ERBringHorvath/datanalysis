import pandas as pd

csv1 = pd.read_csv('file1.csv')
csv2 = pd.read_csv('file2.csv')

merged_df = pd.merge(csv1, csv2, on=['column1', 'column2'])

merged_df.to_csv('merged.csv', index=False)
