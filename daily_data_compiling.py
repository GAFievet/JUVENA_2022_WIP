import os
import pandas as pd

def compiling(directory):
	"""
	:param directory: directory where to find .csv files to compile
	:return: a compiled dataframe
	"""
	dfs=[]
	all_files = os.listdir(directory)
	csv_files = [f for f in all_files if f.endswith('.csv')]
	for file in csv_files:
			# append file
			df = pd.read_csv(os.path.join(directory, file))
			dfs.append(df)

	combined_df = pd.concat(dfs, ignore_index=True)

	return combined_df