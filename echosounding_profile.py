from datetime import datetime

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.io import loadmat

from bv_frequencies import load_dot_mat_CTD, compute_bv_freq, bv_freq_avg_every_k_meters
from filter_lp import get_sampling_freq_total_time, get_cutoff_freq_norm, get_lp_butter_lp_filter_param, lp_filter

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


def extract_curves(bv_matrix, threshold=0.024):
	"""
	Extracts two curves representing the boundaries where BV values exceed a threshold.

	Args:
		bv_matrix (numpy.ndarray): 2D array of BV frequency values (depth x time).
		threshold (float): The threshold value above which to define the curves.

	Returns:
		tuple: A tuple containing two numpy arrays:
			   - upper_boundary (1D array): Depth indices for the upper boundary.
			   - lower_boundary (1D array): Depth indices for the lower boundary.
			   Returns None if no values exceed the threshold.
	"""

	depths, times = bv_matrix.shape

	upper_boundary = np.full(times, np.nan, dtype = float)  # Initialize with NaN
	lower_boundary = np.full(times, np.nan, dtype = float)  # Initialize with NaN

	for t in range(times):
		exceed_indices = [i for i, e in enumerate(bv_matrix[:, t]) if e > threshold]

		if len(exceed_indices) > 0:
			upper_boundary[t] = exceed_indices[0]  # First index above threshold
			lower_boundary[t] = exceed_indices[-1]  # Last index above threshold

	# Handle cases where no threshold is exceeded at a given time:
	# Option 1: Keep NaN and let plotting handle it (gaps in the filled area)
	# Option 2: Interpolate (if you want connected lines even where data is missing)
	# Example of linear interpolation:

	valid_times = ~np.isnan(upper_boundary)
	if np.any(valid_times):  # Check if any valid times exist
		f_upper = interp1d(np.where(valid_times)[0], upper_boundary[valid_times], kind = 'linear',
		                   fill_value = "extrapolate")
		upper_boundary = f_upper(np.arange(times))

		f_lower = interp1d(np.where(valid_times)[0], lower_boundary[valid_times], kind = 'linear',
		                   fill_value = "extrapolate")
		lower_boundary = f_lower(np.arange(times))
	# Make sure it's a list of indices
	upper_boundary = [round(e) for e in upper_boundary]
	lower_boundary = [round(e) for e in lower_boundary]

	return upper_boundary, lower_boundary, threshold


def plot_acoustic_profile(date, mld, bathy, acoustic_df, upper_boundary, lower_boundary, threshold, depth_avg, cf_h):
	# Create figure
	fig, ax1 = plt.subplots(figsize = (15, 4))  # Adjusted figure size
	# Plot TC
	ax1.plot(date, -mld, '-k', linewidth = 1.3, label = 'Thermocline LP 7h')
	# Scatter anchovy schools and add colorbar
	scatter = ax1.scatter(acoustic_df['Time_avg_UTC'], -acoustic_df['Depth_start'], s = 30,
	                      c = 10 * np.log10(acoustic_df['Sv_lin']), marker = 'o', cmap = 'jet')
	cbar = fig.colorbar(scatter, ax = ax1, pad = 0.07)

	# Brunt-Väisälä freq.
	s1 = [depth_avg[e] for e in upper_boundary]
	s2 = [depth_avg[e] for e in lower_boundary]
	# Low pass signals
	sf, length_sec = get_sampling_freq_total_time(s1, 14)
	fc = get_cutoff_freq_norm(cf_h, length_sec)
	a, b = get_lp_butter_lp_filter_param(4, fc)
	s1 = lp_filter(a, b, s1)
	s2 = lp_filter(a, b, s2)

	ax1.fill_between(date, s1, s2, fc = 'red', alpha = 0.2, label = f"BV freq. > {threshold} Hz LP {cf_h}h")

	# Bathymetry
	ax2 = ax1.twinx()  # Create a second y-axis
	ax2.plot(date, bathy, ':k', linewidth = 1)  # Plot bathymetry
	# Add shelf break depth line
	ax2.axhline(-200, linestyle = '-.', color = 'k', linewidth = 0.8)  # yline to axhline

	axes = [ax1, ax2]
	return fig, axes, cbar


def fine_tune_acoustic_profile(ax, cbar, date):
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
	ax[0].legend(lines1 + lines2, labels1 + labels2, loc = 'lower left', framealpha = 1, facecolor = 'white')

	cbar.set_label("VBS (dB)")
	plt.tight_layout()  # Adjust layout to prevent labels from overlapping


if __name__ == "__main__":
	date, cond, depth, lon, lat, pressure, salinity, temp = load_dot_mat_CTD()
	mld = load_dot_mat_mld()
	bathy = load_dot_mat_bathy()
	acoustic_df = load_dot_mat_ancho()
	X1, Y1, n = compute_bv_freq(salinity, temp, pressure, lat, date, depth,)
	X2, Y2, bv_mean, depth_avg = bv_freq_avg_every_k_meters(n, depth, date)
	upper_boundary, lower_boundary, threshold = extract_curves(bv_mean, 0.024)
	fig, ax, cbar = plot_acoustic_profile(date, mld, bathy, acoustic_df, upper_boundary, lower_boundary, threshold,
	                                      depth_avg, 48)
	fine_tune_acoustic_profile(ax, cbar, date)

	plt.savefig(r'C:\Users\G to the A\PycharmProjects\Paper\plots\echosounding_profile.png', transparent = False,
	            bbox_inches = 'tight')

	# plt.show()
