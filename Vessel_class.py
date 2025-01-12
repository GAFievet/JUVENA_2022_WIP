import cartopy.crs as ccrs


class Vessel:
	def __init__(self, longitudes, latitudes, time_stamps):
		"""
		:param longitudes: list of longitudes of the vessel
		:param latitudes: list of latitudes of the vessel
		:param time_stamps: list of datetime related to each coordinates of the vessel
		"""
		self.lons = longitudes
		self.lats = latitudes
		self.time = time_stamps

		# Sets the orientation of the vessel
		if self.lats[0] < self.lats[-1]:
			towards = '^'
		else:
			towards = 'v'
		self.orientation = towards

	def plot_transect(self, a):
		"""
		 Plots the vessel on the provided ax.

		 Args:
		     a: The matplotlib ax object to plot on.
		 """
		a.plot(self.lons, self.lats, transform = ccrs.Geodetic(), label = self.time[0].strftime("%d/%m/%Y"), ls = '-',
		       lw = '1', marker = self.orientation, markevery = (0, -1))
