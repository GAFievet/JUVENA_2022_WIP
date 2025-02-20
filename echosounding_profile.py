from datetime import datetime

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.io import loadmat

from bv_frequencies import load_dot_mat_CTD

CTD_path = r'C:\Users\G to the A\Desktop\MT\Programming\CTD'
CTD_file_name = 'PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat'

TC_path = r"C:\Users\G to the A\Desktop\MT\Programming\Accoustic\Thermocline_data"

Bathy_path = r"C:\Users\G to the A\Desktop\MT\Programming\Accoustic"

ancho_path = r"C:\Users\G to the A\Desktop\MT\Programming\Accoustic\MATLAB RESULTS\Datasets making - stats"


def load_dot_mat_mld(MLD_path=TC_path, MLD_file_name="MLD_filtered.mat"):
	# Load data
	data_mld_filtered = loadmat(f"{MLD_path}\\{MLD_file_name}", squeeze_me = True)
	mld = data_mld_filtered['MLD_7h_LP'][0:915].reshape(-1, 1).flatten()

	return mld


def load_dot_mat_bathy(bathy_path=Bathy_path, bathy_file_name="floor_depth_profile_2309_0610.mat"):
	data_bathy = loadmat(f"{bathy_path}\\{bathy_file_name}")
	bathy = data_bathy['bathy_profile'].reshape(-1, 1).flatten()

	return bathy


def load_dot_mat_ancho(ancho_path=ancho_path, ancho_file_name="Juvenile_Anchovy_datasets_Sv_lin.csv"):
	acoustic_df = pd.read_csv(f"{ancho_path}\\{ancho_file_name}")
	acoustic_df = acoustic_df[acoustic_df['Sv_lin'] != 0]  # Filter out null values
	acoustic_df['Time_avg_UTC'] = pd.to_datetime(acoustic_df['Time_avg_UTC'], format = '%d-%b-%Y %H:%M:%S')

	return acoustic_df



def plot_acoustic_profile(date, depth, mld, bathy, acoustic_df):
	# Create figure
	fig, ax1 = plt.subplots(figsize = (15, 4))  # Adjusted figure size
	# Plot TC
	ax1.plot(date, -mld, '-k', linewidth = 1.3, label = 'Thermocline LP 7h')
	# Scatter anchovy schools and add colorbar
	scatter = ax1.scatter(acoustic_df['Time_avg_UTC'], -acoustic_df['Depth_start'], s = 30,
	                      c = 10 * np.log10(acoustic_df['Sv_lin']), marker = 'o', cmap = 'jet')
	cbar = fig.colorbar(scatter, ax = ax1, pad = 0.07)

	# Bathymetry
	ax2 = ax1.twinx()  # Create a second y-axis
	ax2.plot(date, bathy, ':k', linewidth = 1, label = 'Bathymetry')  # Plot bathymetry
	# Add shelf break depth line
	ax2.axhline(-200, linestyle = '-.', color = 'k', linewidth = 0.8)  # yline to axhline

	# ax1.fill_between([storm_start, storm_end], yl[1], yl[1], yl[0], color = 'blue', alpha = 0.1, label = 'Storm')

	axes = [ax1, ax2]
	return fig, axes, cbar


def fine_tune_acoustic_profile(fig, ax, cbar, date):
	# Axis labels and limits
	ax[0].set_ylabel("Thermocline & Juvenile Anchovy depth (m)")
	ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
	ax[0].xaxis.set_major_locator(mdates.DayLocator(interval = 1))
	ax[0].set_xlim(date[0], date[-1])  # Corrected index
	ax[0].set_ylim(-60, 0)
	# Second y-axis
	ax[1].set_ylabel("Sea floor depth (m)", labelpad = 10)
	ax[1].get_legend_handles_labels()  # dummy call to update legend
	ax[1].text(x = date[-1], y = -200, s = 'Shelf break', ha = 'right', va = 'bottom')

	# Add storm indication
	storm_start = datetime.strptime("26/09/2022 00:00:00", "%d/%m/%Y %H:%M:%S")
	storm_end = datetime.strptime("30/09/2022 23:59:59", "%d/%m/%Y %H:%M:%S")
	ymin, ymax = ax[0].get_ylim()
	l = storm_end - storm_start
	rect = plt.Rectangle((storm_start, ymin), l, abs(ymax - ymin), facecolor = 'blue', alpha = 0.1, label = "Storm")
	ax[0].add_patch(rect)  # Red frame

	# Combine legends from both axes
	lines1, labels1 = ax[0].get_legend_handles_labels()
	lines2, labels2 = ax[1].get_legend_handles_labels()
	ax[0].legend(lines1 + lines2, labels1 + labels2, loc = 'lower right')

	cbar.set_label("VBS (dB)")

	return


if __name__ == "__main__":
	date, cond, depth, lon, lat, pressure, salinity, temp = load_dot_mat_CTD()
	mld = load_dot_mat_mld()
	bathy = load_dot_mat_bathy()
	acoustic_df = load_dot_mat_ancho()
	fig, ax, cbar = plot_acoustic_profile(date, depth, mld, bathy, acoustic_df)
	fine_tune_acoustic_profile(fig, ax, cbar, date)

	plt.tight_layout()  # Adjust layout to prevent labels from overlapping
	plt.show()
