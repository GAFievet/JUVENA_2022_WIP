import cartopy.crs as ccrs
import matplotlib.dates as mdates
from datetime import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pickle
import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


class Glider:
	def __init__(self, longitudes, latitudes, time_stamps):
		"""
		:param longitudes: list of longitudes of the glider
		:param latitudes: list of latitudes of the glider
		:param time_stamps: list of datetime (UTC) related to each coordinates of the glider
		"""
		self.lons = longitudes
		self.lats = latitudes
		self.time = time_stamps

	def plot_transect(self, figure, a):
		"""
		:param figure: figure to plot on
		:param a: Set of axes
		:return: plots the glider path with colour according to the time and adds a colorscale.
		"""

		# Convert dates to matplotlib-compatible format
		normalized_time = mdates.date2num(self.time)

		# Create a scatter plot with color based on datetime
		sc = a.scatter(self.lons, self.lats, c = normalized_time, cmap = 'viridis', transform = ccrs.Geodetic(),
		               s = 10)

		# Add a colorbar with a matching colormap
		cbar = figure.colorbar(sc, ax = a, fraction = 0.042, orientation = 'vertical')

		# # Data processing limits
		# # Define the target date
		# end = datetime(2022, 10, 7, 0, 0, 0).date() # Extract only the date part
		# try:
		# 	iend = next(i for i, dt in enumerate(self.time) if dt.date() == end)
		# 	iend = iend - 1
		# except StopIteration:
		# 	return "Iterration in glider_GPS extracted data issue"

		# Set label to color bar
		cbar.set_label('Time')

		# Define ticks
		ticks = normalized_time[::len(normalized_time) // 6]
		# Set the ticks explicitly
		cbar.set_ticks(ticks)
		# Set tick labels
		cbar.set_ticklabels([mdates.num2date(tick).strftime("%d/%m/%Y") for tick in ticks])

		# # Create a rectangle to highlight the range
		# vmax=ticks[4]
		# cbar.ax1.add_patch(plt.Rectangle((0, 0), 1, vmax , facecolor = 'none', edgecolor = 'red', linewidth
		# = 2))
# Plot the path as a line
# a.plot(self.lons, self.lats, transform = ccrs.Geodetic(), c = 'k', ls = '-', lw = 0.5)
