import os
import pickle

import pandas as pd

from src import config
from src.core.datetime_formating import combine_date_time


def extract_vessel_echo_data(file, saving_path):
	"""
	:param saving_path: path where to save the .pkl file
	:param file: string of the path of an Excel extraction_file containing  vessel transects vessel_mat
	:return: list [longitudes,latitudes,time_stamps] (i.e., args for plot_vessel_transect class)
	"""
	df = pd.read_csv(file)
	vessel_mat = [df['Lon_M'].tolist(), df['Lat_M'].tolist(), df['Date_M'].tolist(), df['Time_M'].tolist()]
	vessel_mat[2] = combine_date_time(vessel_mat[2], vessel_mat[3])
	vessel_mat.pop(3)

	# Save the matrix to an extraction_file
	with open(os.path.join(saving_path, file[-30:-20] + '.pkl'), 'wb') as f:
		# noinspection PyTypeChecker
		pickle.dump(vessel_mat, f)

	return vessel_mat


if __name__ == "__main__":
	vessel_0904 = extract_vessel_echo_data(os.path.join(config.RAW_VESSEL_ECHO, 'EB20220904_fullwatercolumn.csv'),
	                                       config.VESSEL_ECHO)
	vessel_0930 = extract_vessel_echo_data(os.path.join(config.RAW_VESSEL_ECHO, 'RM20220930_fullwatercolumn.csv'),
	                                       config.VESSEL_ECHO)
	vessel_1001 = extract_vessel_echo_data(os.path.join(config.RAW_VESSEL_ECHO, 'RM20221001_fullwatercolumn.csv'),
	                                       config.VESSEL_ECHO)
