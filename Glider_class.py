import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


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

		# dt = (self.time[-1] - self.time[0])
		# normalized_time = [(t - self.time[0]) / dt for t in self.time]

		# Convert dates to matplotlib-compatible format
		normalized_time = mdates.date2num(self.time)

		# Create a scatter plot with color based on datetime
		sc = a.scatter(self.lons, self.lats, c = normalized_time, cmap = 'viridis', transform = ccrs.Geodetic(),
		               s = 10)

		# Add a colorbar with a matching colormap
		cbar = figure.colorbar(sc, ax = a, orientation = 'vertical')
		cbar.set_label('Time')

		# Define ticks
		ticks = normalized_time[::len(normalized_time) // 6]
		# Set the ticks explicitly
		cbar.set_ticks(ticks)
		# Set tick labels
		cbar.set_ticklabels([mdates.num2date(tick).strftime("%d/%m/%Y") for tick in ticks])

# Plot the path as a line
# a.plot(self.lons, self.lats, transform = ccrs.Geodetic(), c = 'k', ls = '-', lw = 0.5)
