import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime_formating import combine_date_time
import pickle
import os
from datetime import datetime


def extract_vessel_fishing_data(file, saving_path, haul):
	"""
	:param haul: type int, Haul number to retreive
	:param saving_path: path where to save the .pkl file
	:param file: string of the path of an Excel extraction_file containing  vessel transects vessel_mat
	:return: list [longitudes,latitudes,time_stamps] (i.e., args for plot_vessel_transect class)
	"""
	df = pd.read_excel(file)
	haul_row = df[df['HAUL'] == haul]
	if not haul_row.empty:  # If the haul exist in the file and is unique.
		# Creates loc_i and loc_f lists of coordinates
		loc_i = [
			haul_row['iLong_cent'].iloc[0] if not pd.isna(haul_row['iLong_cent'].iloc[0]) else None,
			haul_row['iLat_cent'].iloc[0] if not pd.isna(haul_row['iLat_cent'].iloc[0]) else None,
		]
		loc_f = [
			haul_row['fLong_cent'].iloc[0] if not pd.isna(haul_row['fLong_cent'].iloc[0]) else None,
			haul_row['fLat_cent'].iloc[0] if not pd.isna(haul_row['fLat_cent'].iloc[0]) else None,
		]

		# Collect date of the trawl
		date = haul_row['fecha'].iloc[0]

		# COLLECT DATA FOR ABUNDANCE PIE CHARTS
		# Get fish column indexes
		fish_i_f = df.columns.get_indexer(['ANE', 'OT'])
		# Get fish species acronyms
		species = df.columns[fish_i_f[0]:fish_i_f[1]]

		# Import colors for pie charts
		with open(r'/vessel_fishing/color_palette.pkl', 'rb') as f:
			colors = pickle.load(f)

		# Get fishes mass captured in a list and convert nan into 0 and name list aswell
		masses_fished = haul_row.iloc[0, fish_i_f[0]:fish_i_f[1]].tolist()
		species = [sp for sp, m in zip(species, masses_fished) if m != 0]
		colors = [c.tolist() for c, m in zip(colors, masses_fished) if m != 0]
		masses_fished = [float(m) for m in haul_row.iloc[0, fish_i_f[0]:fish_i_f[1]].tolist() if m != 0]

		fishing_dict = {
			'loc_i': loc_i, 'loc_f': loc_f, 'date': date, 'species': species,
			'masses': masses_fished, 'color palette': colors
		}
		#  loc_i and loc_f are inital and end location of the vessel conducting the trawl formatted as [longitude,
		#  latitude].
		# species is the list of acronyms (as str) for all species that could be fished
		# mass_fishes is a list of same length and order as species containg the propotion of each species fished
		# during the trawl.

		# Save the dictionary to an extraction_file
		with open(os.path.join(saving_path, f'haul_{haul}' + '.pkl'), 'wb') as f:
			# noinspection PyTypeChecker
			pickle.dump(fishing_dict, f)

		return fishing_dict

	else:  # Raises and error if the haul is not found
		raise ValueError(f"No rows found for HAUL: {haul}")


if __name__ == "__main__":
	save = r'../data/vessel_fishing'
	file_name = r'../data/vessel_fishing/fishing operatiions V6 V8 V10.xlsx'
	example_dict = extract_vessel_fishing_data(file_name, save, 9001)
	# with open(r'C:\Users\G to the A\PycharmProjects\Paper\vessel_fishing\haul_9048.pkl', 'rb') as f:
	# 	example_dict = pickle.load(f)
	# print(example_dict)
	# print(type(example_dict))
	# print(example_dict['color palette'])
	# print(sum(example_dict['masses']))
	# print(type(example_dict['masses'][0]))
	# print(example_dict['species'])


# cmap = plt.colormaps.get_cmap('hsv')
# values = np.linspace(0, 1, 31)
# # Get the colors from the colormap
# colors = cmap(values)
#
# # print(colors)
# with open(os.path.join(save, 'color_palette.pkl'), 'wb') as f:
# 	pickle.dump(colors, f)
