import cartopy.crs as ccrs
import matplotlib.pyplot as plt

class Vessel_fishing:
	def __init__(self, loc_i, loc_f, time_stamp, species, mass_fished, colors):
		"""
		:type colors: color palette
		:param loc_i: init [longitude, latitude]
		:param loc_f: end [longitude, latitude]
		:param time_stamp: Date (datetime object)
		:param species: List of species fished as str acronyms
		:param mass_fished: list of proportion for each of these species (sum~1)
		"""
		self.colors = colors
		self.lons = [-loc_i[0], -loc_f[0]]
		self.lats = [loc_i[1], loc_f[1]]
		self.time = time_stamp
		self.species = species
		self.mass_fished = mass_fished

		# Sets the orientation of the vessel
		if self.lats[0] < self.lats[-1]:
			towards = '^'
		else:
			towards = 'v'
		self.orientation = towards

	def plot_transect(self, a):
		"""
		 Plots the vessel on the provided ax1.

		 Args:
		     a: The matplotlib ax1 object to plot on.
		 """
		a.plot(self.lons, self.lats, transform = ccrs.Geodetic(), label = self.time.strftime("%d/%m/%Y"), ls = '--',
		       lw = '1', marker = self.orientation, markevery = [0, - 1])

	def abundance_pie_chart(self, a):
		"""
		:type a: Set of axis to plot on
		:return: a pie chart of the relative abundance of fish species
		"""
		wedges, percentages = a.pie(self.mass_fished, labels = self.species, colors = self.colors,
		                                    startangle = 140)
		plt.title(self.time.strftime("%d/%m/%Y"))
		a.axis('equal')

		# Hide percentages and labels
		for percentage in percentages:
			percentage.set_visible(False)
		# for wedge in wedges:
		# 	wedge.set_visible(False)

		# Calculate and display the number of slices
		a.text(0, 0, f"{len(self.species)}", horizontalalignment = 'center', verticalalignment = 'center',
		       fontsize = 13)

