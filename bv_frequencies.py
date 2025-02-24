import os
from datetime import datetime, timedelta

import gsw  # Use gsw instead of seawater
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from matplotlib.ticker import MultipleLocator


# from matplotlib.text import Text
# from mpl_toolkits.axes_grid1 import make_axes_locatable

CTD_path = r'C:\Users\G to the A\Desktop\MT\Programming\CTD'
CTD_file_name = 'PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat'

def load_dot_mat_CTD(CTD_path=CTD_path, CTD_file_name=CTD_file_name):
	"""
	:param path: path of the file
	:param file_name: .mat file
	:return: date, cond, depth, lon, lat, pressure, salinity, temp arrays
	"""
	# Load data from .mat file
	p = os.path.join(CTD_path, CTD_file_name)
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


def compute_bv_freq(salinity, temp, pressure, lat,date,depth):
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
		n_slice = n[:, i:i + k]  # Create (depth) slices to average
		n_slice[np.all(np.isnan(n_slice), axis = 1)] = -999  # Attribute an outlier value to elements in full NaN rows
		bv_mean.append(np.nanmean(n_slice, axis = 1))  # Compute rows mean
		n_slice[n_slice == -999] = np.nan  # Attribute an outlier value to elements in full NaN rows
		depth_avg[i // k] = np.nanmean(depth[i:i + k])  # Compute depth mean

	bv_mean = np.array(bv_mean)
	bv_mean[bv_mean == -999] = np.nan  # Get the outlier mean back to nan
	# FORMAT DATA FOR PLOTTING
	X2, Y2 = np.meshgrid(date, depth_avg)

	return X2, Y2, bv_mean, depth_avg


def bv_sum_top_k_meters(n, k=70):
	"""
	:param n: bv freq matrix
	:param k: sum over k meters (default = 70m)
	:return: BV freq summed over k meters (array)
	Sum of BV of the first k m of each profile as a measure of stratification
	"""
	sBV = np.nansum(n[:, 0:k], axis = 1)

	return sBV


def bvsubplots(date, X1, Y1, n, X2, Y2, bv_mean, sBV):
	"""
	:return: sets of axes and fig
	"""
	n = n.T
	to_plot = [[X1, Y1, n], [X2, Y2, bv_mean], [date, sBV]]
	###################### CREATE FIG ######################
	# Create fig
	fig = plt.figure(figsize = (8, 8))
	# Use GridSpec for layout control
	gs = gridspec.GridSpec(3, 1)

	# Store axes and colorbars in lists
	axes = []
	cbars = []

	for i in range(3):
		ax = fig.add_subplot(gs[i])
		axes.append(ax)

		if i == 2:
			ax.plot(to_plot[-1][0], to_plot[-1][1], '-b', lw = 1)
		else:
			# CONTOUR
			contourf = ax.contourf(to_plot[i][0], to_plot[i][1], to_plot[i][2], 30, cmap = 'jet')
			# COLORBAR
			# Create inset axes
			cbar_ax = ax.inset_axes([1.05, 0.05, 0.03, 0.9], transform = ax.transAxes)  # [left, bottom, width, height]
			# Init. cbar
			cbar = fig.colorbar(contourf, cax = cbar_ax, orientation = 'vertical')
			cbars.append(cbar)

	return fig, axes, cbars


def fine_tune_subplots(fig, axes, cbars, max_depth_shown=210):
	"""
	:param fig:
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
	text = ["a)", "b)", "c)"] # Add letter to refer to each subplot
	fig.subplots_adjust(left = 0.15, right = 0.85, bottom = 0.05, top = 0.95, wspace = 0, hspace = 0.1)

	for i, ax in enumerate(axes):

		axes[i].text(-0.12, 0.9, text[i], fontsize = 11, fontweight = 'bold', transform = axes[i].transAxes)

		if ax == axes[2]:
			ax.set_ylim([0, 0.7])
			# ax.set_box_aspect(0.16)
			ax.yaxis.set_major_locator(MultipleLocator(0.1))
			ax.set_ylabel(r'BV freq. (Hz)')
			# Show grid
			ax.grid(visible = True, which = 'both', axis = 'y')
			ymin, ymax = ax.get_ylim()
			rect = plt.Rectangle((storm_start, ymin), l, abs(ymax - ymin), facecolor = 'none', edgecolor = 'red',
			                     lw = 2)
			axes[2].add_patch(rect)  # Red frame
		else:
			# Hide x-axis ticks for top 2 charts
			ax.tick_params(axis = 'x', which = 'both', labelbottom = False)
			# Add grid
			ax.grid(visible = True, which = 'major', axis = 'both', ls = ':')
			# Cbar
			# Format colorbar ticks in scientific notation
			cbars[i].formatter.set_scientific(True)  # Turn on scientific notation
			cbars[i].formatter.set_powerlimits((0, 0))  # Set limits for when to use scientific notation (optional)
			cbars[i].update_normal() # Important: Update the colorbar to apply the formatter
			cbars[i].set_label(r'BV freq. (Hz)')
			ax.set_ylabel('Depth (m)')
			# Set ylim
			ax.set_ylim([ylim, 0])
		# Set box aspect
		# ax.set_box_aspect(0.1)

		# To create custom evenly spaced xticks
		# axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b-%d %H:%M'))
		# axes[0].set_xticks(np.linspace(date_num.min(), date_num.max(), 9))
		ax.xaxis.set_major_locator(locator)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
		ax.set_xlim([date_num.min(), date_num.max()])
		# Allow LaTeX use for labels in plt
		# text = Text(storm_start + l / 2, ylim + 10 * 100 / abs(ylim), 'Storm', ha = 'center', va = 'center',
		# color = 'red',
		# fontsize = 11, )
		# ax.add_artist(text)  # Text
		rect = plt.Rectangle((storm_start, ylim), l, abs(ylim), facecolor = 'none', edgecolor = 'red', lw = 2)
		ax.add_patch(rect)  # Red frame



if __name__ == "__main__":
	date, cond, depth, lon, lat, pressure, salinity, temp = load_dot_mat_CTD()
	X1, Y1, n = compute_bv_freq(salinity, temp, pressure, lat,date,depth)
	X2, Y2, bv_mean, depth_avg = bv_freq_avg_every_k_meters(n, depth, date)
	sBV = bv_sum_top_k_meters(n, 30)
	fig, axes, cbars = bvsubplots(date, X1, Y1, n, X2, Y2, bv_mean, sBV)
	fine_tune_subplots(fig, axes, cbars, max_depth_shown = 210)

	# Save fig
	plt.savefig(r'C:\Users\G to the A\PycharmProjects\Paper\plots\BV_frequencies.png', transparent = False,
	            bbox_inches = 'tight')

	# Plot full size
	# plt.show()