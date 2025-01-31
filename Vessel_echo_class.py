import cartopy.crs as ccrs


class Vessel_echo:
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

	def plot_transect(self, a2,lon_shift):
		"""
		:type fig: figure
		:param a2: Child axis
		:param lon_shift: dlongitude to spread transects horizontally
		:return: plots a transect of vessel fishing
		"""
		new_lons = [lon + lon_shift for lon in self.lons]
		a2.plot(new_lons, self.lats, transform = ccrs.Geodetic(), label = self.time[len(self.time) // 2].strftime(
			"%d/%m/%Y"), ls = '-', lw = '1', marker = self.orientation, markevery = [0, - 1])

