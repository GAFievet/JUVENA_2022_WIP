import pandas as pd
from datetime_formating import combine_date_time


def extract_vessel_data(file):
	"""
	:param file: string of the path of an Excel extraction_file containing  vessel transects data
	:return: list [longitudes,latitudes,time_stamps] (i.e., args for plot_vessel_transect class)
	"""
	df = pd.read_csv(file)
	data = [df['Lon_M'].tolist(), df['Lat_M'].tolist(), df['Date_M'].tolist(), df['Time_M'].tolist()]
	data[2] = combine_date_time(data[2], data[3])
	data.pop(3)
	return data


if __name__ == "__main__":
	vessel_0904 = extract_vessel_data('EB20220904_fullwatercolumn.csv')
	vessel_0930 = extract_vessel_data('RM20220930_fullwatercolumn.csv')
	vessel_1001 = extract_vessel_data('RM20221001_fullwatercolumn.csv')
