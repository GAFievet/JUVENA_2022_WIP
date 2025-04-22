from datetime import datetime

import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.text import Text


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

		# Set label to color bar
		cbar.set_label('Time')

		# Define ticks
		ticks = normalized_time[::len(normalized_time) // 6]
		# Set the ticks explicitly
		cbar.set_ticks(ticks)
		# Set tick labels
		cbar.set_ticklabels([mdates.num2date(tick).strftime("%d/%m/%Y") for tick in ticks])

		# Create a rectangle to highlight the range
		y = datetime(2022, 9, 26, 0, 0, 0).date()  # Extract only the date part
		h = datetime(2022, 10, 1, 0, 0, 0).date()  # Extract only the date part
		rect = plt.Rectangle((0, y), 1, h - y, facecolor = 'none', edgecolor = 'red', lw = 2)
		cbar.ax.add_patch(rect)

		# Calculate center coordinates of the centre of the rectangle
		x_center = rect.get_x() + rect.get_width() / 2
		y_center = rect.get_y() + rect.get_height() / 2

		# Create text object
		text = Text(x_center, y_center, 'Storm', ha = 'center', va = 'center', color = 'red', fontsize = 11,
		            rotation = 90)

		# Add text to the plot
		cbar.ax.add_artist(text)
