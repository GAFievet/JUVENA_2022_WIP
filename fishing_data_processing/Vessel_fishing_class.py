import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

from closest_point_on_edge import get_closest_point_on_edge


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

	def plot_transect(self, a, lon_shift):
		"""
		:param a: axis to plot on
		:param lon_shift: dlongitude to spread transects horizontally
		:return: plots a transect of vessel fishing
		"""
		new_lons = [lon + lon_shift for lon in self.lons]
		a.plot(new_lons, self.lats, transform = ccrs.Geodetic(), label = self.time.strftime("%d/%m/%Y"),
		       ls = '--', lw = '1', marker = self.orientation, markevery = [0, - 1])

	def abundance_pie_chart(self, a1, a2, vessel_loc):
		"""
		:param vessel_loc: coordinates (a1) of the vessel location to link to the pie chart [lon,lat]
		:param a1: Set of axes for the map
		:param a2: Set of axes for the pie chart
		:return: a pie chart of the relative abundance of fish species
		"""
		wedges, percentages = a2.pie(self.mass_fished, labels = self.species, colors = self.colors,
		                             startangle = 140)
		plt.title(self.time.strftime("%d/%m/%Y"), fontsize = 11, pad = 0.5)
		a2.axis('equal')

		# Hide percentages and labels
		for percentage in percentages:
			percentage.set_visible(False)
		# for wedge in wedges:
		# 	wedge.set_visible(False)

		# Calculate and display the number of slices
		a2.text(0, 0, f"{len(self.species)}", horizontalalignment = 'center', verticalalignment = 'center',
		        fontsize = 13)

		a2.legend()

		# --- Find the closest point on the pie chart to the point on the map ---
		# 1. Get the center of the pie chart
		pie_center = (a2.get_xlim()[0] + a2.get_xlim()[1]) / 2, (a2.get_ylim()[0] + a2.get_ylim()[1]) / 2

		# 2. Calculate the distance from the point to the center of the pie chart
		distance_to_center = np.sqrt((vessel_loc[0] - pie_center[0]) ** 2 + (vessel_loc[1] - pie_center[1]) ** 2)

		closest_point_on_pie = get_closest_point_on_edge((vessel_loc[0], vessel_loc[1]), pie_center, a2.get_xlim()[1] -
		                                                 pie_center[0])

		# --- Plot the line connecting the points ---
		# Use the Mercator coordinates for both points
		a1.plot([vessel_loc[0], closest_point_on_pie[0]], [vessel_loc[1], closest_point_on_pie[1]], 'k--', lw=8,
		        transform = a1.transData)
