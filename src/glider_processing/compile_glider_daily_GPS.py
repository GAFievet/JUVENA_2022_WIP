import os
import pandas as pd
from src.core.datetime_formating import combine_date_time

"""
Compiles daily glider GPS .csv files and format the date and time.
"""

directory = r'../data/glider/Daily_GPS'
dfs = []
all_files = os.listdir(directory)
csv_files = [f for f in all_files if f.endswith('.csv')]
for file in csv_files:
	# append extraction_file
	df_daily = pd.read_csv(os.path.join(directory, file))
	dfs.append(df_daily)

combined_df = pd.concat(dfs, ignore_index = True)

# Combine dates and times into datetime object (result is a list)
new_datetimes = combine_date_time(combined_df['GPS_date'].tolist(), combined_df['GPS_time'].tolist())
# Insert it as a pandas.Series object in combined_df
combined_df['GPS_date']=pd.Series(new_datetimes)
# Delete GPS_time series in combined_df
del combined_df['GPS_time']
# Sort the combined DataFrame by the 'GPS_date' column
combined_df.sort_values(by = 'GPS_date', inplace = True)
# Save combined_df
combined_df.to_csv(r'../data/glider/glider.gps.csv', index = False)
