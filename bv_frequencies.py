import os
from datetime import datetime, timedelta

import gsw  # Use gsw instead of seawater
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from matplotlib.ticker import MultipleLocator


# from matplotlib.text import Text
# from mpl_toolkits.axes_grid1 import make_axes_locatable

def load_dot_mat(path, file_name):
	"""
	:param path: path of the file
	:param file_name: .mat file
	:return: date, cond, depth, lon, lat, pressure, salinity, temp arrays
	"""
	# Load data from .mat file
	p = os.path.join(path, file_name)
	data = sio.loadmat(p, squeeze_me = True)  # Squeeze arrays to avoid singletons
	# Init. clear variables
	date = data['time'][0:915]
	cond = data['conductivity'][0:915]
	depth = data['depth']
	lon = data['longitude'][0:915]
	lat = data['latitude'][0:915]
	pressure = data['pressure'][0:915]
	salinity = data['salinity'][0:915]
	temp = data['temperature'][0:915]
	# Convert to python-readable datetime
	date = [(datetime(1, 1, 1) + timedelta(days = matlab_date - 367)) for matlab_date in date]

	return date, cond, depth, lon, lat, pressure, salinity, temp


def compute_bv_freq(salinity, temp, pressure, lat):
	"""
	:return: X1 (time) and Y1 (depth) as meshgrid and n the bv frequencies over the meshgrid
	"""
	n2, p = gsw.Nsquared(salinity.T, temp.T, pressure.T, lat.T)
	n = np.sqrt(np.abs(n2.T))  # Transpose n2 back and calculate N
	n[np.isinf(n)] = np.nan
	# n[n < 0.025] = np.nan # Filter frequencies
	# FORMAT DATA FOR PLOTTING
	X1, Y1 = np.meshgrid(date, depth[0:-1])

	return X1, Y1, n


def bv_freq_avg_every_k_meters(n, depth, date, k=5):
	"""
	:param date:
	:param depth:
	:param n: bv freq matrix
	:param k: average every k meters (default = 5)
	"""
	depth_avg = [[] for _ in range(210 // k)]
	bv_mean = []
	for i in range(1, 210, k):

		n_slice = n[:, i:i + k]  # Create (temporal) slices to average
		n_slice[np.all(np.isnan(n_slice), axis = 1)] = -999  # Attribute an outlier value to elements in full NaN rows
		bv_mean.append(np.nanmean(n_slice, axis = 1))  # Compute rows mean
		n_slice[n_slice == -999] = np.nan  # Attribute an outlier value to elements in full NaN rows
		depth_avg[i // k] = np.nanmean(depth[i:i + k])  # Compute depth mean

	bv_mean = np.array(bv_mean)
	bv_mean[bv_mean == -999] = np.nan  # Get the outlier mean back to nan
	# FORMAT DATA FOR PLOTTING
	X2, Y2 = np.meshgrid(date, depth_avg)

	return X2, Y2, bv_mean


def bv_sum_top_k_meters(n, k=70):
	"""
	:param n: bv freq matrix
	:param k: sum over k meters (default = 70m)
	:return: BV freq summed over k meters (array)
	"""
	sBV = np.nansum(n[:, 0:k], axis = 1)

	return sBV


def bvsubplots(date, X1, Y1, n, X2, Y2, bv_mean, sBV):
	"""
	:return: sets of axes and fig
	"""
	n=n.T
	to_plot = [[X1, Y1, n], [X2, Y2, bv_mean], [date, sBV]]
	###################### CREATE FIG ######################

	fig, axes = plt.subplots(3, 1, figsize = (11, 5))
	# Store colorbars in a list
	cbars = []  # Initialize an empty list

	for i, ax in enumerate(axes):
		if ax == axes[2]:
			ax.plot(to_plot[-1][0], to_plot[-1][1], '-b', lw = 1)
		else:
			# CONTOUR
			contourf = ax.contourf(to_plot[i][0], to_plot[i][1], to_plot[i][2], 30, cmap = 'jet')
			# COLORBAR
			cbar = fig.colorbar(contourf, ax = ax, orientation = 'vertical')
			cbars.append(cbar)

	return fig, axes, cbars


def fine_tune_subplots(axes, cbars, max_depth_shown=210):
	"""
	:param cbars:
	:param axes:
	:param max_depth_shown: default (and max) = 210
	"""
	# Indicate the storm with a red frame
	storm_start = mdates.date2num(datetime(2022, 9, 26))
	storm_end = mdates.date2num(datetime(2022, 9, 30))
	l = storm_end - storm_start
	locator = mdates.AutoDateLocator()  # Automatically find tick positions
	date_num = mdates.date2num(date)
	ylim = -max_depth_shown

	# Adjust inter-plot padding
	# plt.subplots_adjust(hspace = 1)

	for i, ax in enumerate(axes):
		if ax == axes[2]:
			ax.set_ylim([0.6, 1.1])
			ax.set_box_aspect(0.16)
			ax.yaxis.set_major_locator(MultipleLocator(0.1))
			# Show grid
			ax.grid(visible = True, which = 'both', axis = 'y')
			ymin, ymax = ax.get_ylim()
			rect = plt.Rectangle((storm_start, ymin), l, abs(ymax - ymin), facecolor = 'none', edgecolor = 'red',
			                     lw = 2)
			axes[2].add_patch(rect)  # Red frame
		else:
			cbars[i].set_label('BV freq. (rad/s)')
			# Set ylim
			ax.set_ylim([ylim, 0])
			# Set box aspect
			ax.set_box_aspect(0.1)

		# To create custom evenly spaced xticks
		# axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b-%d %H:%M'))
		# axes[0].set_xticks(np.linspace(date_num.min(), date_num.max(), 9))
		ax.xaxis.set_major_locator(locator)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
		ax.set_ylabel('Depth (m)')
		ax.set_xlabel('Time')
		ax.set_xlim([date_num.min(), date_num.max()])

		# text = Text(storm_start + l / 2, ylim + 10 * 100 / abs(ylim), 'Storm', ha = 'center', va = 'center',
		# color = 'red',
		# fontsize = 11, )
		# ax.add_artist(text)  # Text
		rect = plt.Rectangle((storm_start, ylim), l, abs(ylim), facecolor = 'none', edgecolor = 'red', lw = 2)
		ax.add_patch(rect)  # Red frame

	# Layout
	# plt.tight_layout(rect=[0, 0, 1, 0.95])


if __name__ == "__main__":
	path = r'C:\Users\G to the A\Desktop\MT\Programming\CTD'
	file_name = 'PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat'
	date, cond, depth, lon, lat, pressure, salinity, temp = load_dot_mat(path, file_name)
	X1, Y1, n = compute_bv_freq(salinity, temp, pressure, lat)
	X2, Y2, bv_mean = bv_freq_avg_every_k_meters(n, depth, date)
	sBV = bv_sum_top_k_meters(n, 70)
	fig, axes, cbars = bvsubplots(date, X1, Y1, n, X2, Y2, bv_mean, sBV)
	fine_tune_subplots(axes, cbars, max_depth_shown = 210)

# Save fig
plt.savefig(r'C:\Users\G to the A\PycharmProjects\Paper\plots\BV_frequencies.png', transparent = False,
            bbox_inches = 'tight')

# Plot full size
plt.show()
