import cartopy.crs as ccrs

class Glider:
	def __init__(self,longitudes,latitudes,time_stamps):
		"""
		:param longitudes: list of longitudes of the glider
		:param latitudes: list of latitudes of the glider
		:param time_stamps: list of datetime (UTC) related to each coordinates of the glider
		"""
		self.lons=longitudes
		self.lats=latitudes
		self.time=time_stamps

	def plot_transect(self, figure, a):
		"""
		:param figure: figure to plot on
		:param a: Set of axes
		:return: plots the glider path with colour according to the time and adds a colorscale.
		"""

		# Create a scatter plot with color based on datetime
		sc = a.scatter(self.lons, self.lats, c=self.time, cmap='viridis', transform=ccrs.Geodetic(), s=10)

		# Add a colorbar with a matching colormap
		cbar = figure.colorbar(sc, ax=a, orientation='vertical')
		cbar.set_label('Time')

		# Plot the path as a line
		a.plot(self.lons, self.lats, transform=ccrs.Geodetic(), c='k', ls='-',lw=0.5)