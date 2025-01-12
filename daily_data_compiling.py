import os
import pandas as pd

"""
Compiles daily glider GPS .csv files
"""

directory = r'C:\Users\G to the A\PycharmProjects\Paper\glider\Daily'
dfs = []
all_files = os.listdir(directory)
csv_files = [f for f in all_files if f.endswith('.csv')]
for file in csv_files:
	# append extraction_file
	df_daily = pd.read_csv(os.path.join(directory, file))
	dfs.append(df_daily)

combined_df = pd.concat(dfs, ignore_index = True)
combined_df.to_csv(r'C:\Users\G to the A\PycharmProjects\Paper\glider\Glider.gps.csv', index = False)
