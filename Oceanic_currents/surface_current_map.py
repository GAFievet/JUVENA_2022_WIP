import datetime
import pickle

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


def plot_oceanic_currents(u, v, lons, lats, date):
	"""
	Plots surface oceanic current velocities based on u and v components.

	Args:
		u (numpy.ndarray): 2D NumPy array of u-component velocity.
		v (numpy.ndarray): 2D NumPy array of v-component velocity.
		lons (numpy.ndarray): 1D NumPy array of longitude values.
		lats (numpy.ndarray): 1D NumPy array of latitude values.
		date (datetime.datetime): Date associated with the measurements.
	"""

	# 1. Set the figure size
	plt.figure(figsize = (10, 8))

	# 2. Define the map projection (PlateCarree) - Changed from Mercator
	ax = plt.axes(projection = ccrs.PlateCarree())

	# 3. Set the extent of the plot (longitude and latitude limits)
	lonlim = [-5, -1]
	latlim = [43, 45]
	ax.set_extent(lonlim + latlim, crs = ccrs.Geodetic())

	# 4. Add land features to the plot
	ax.add_feature(cfeature.LAND, facecolor = 'lightgray')
	ax.add_feature(cfeature.COASTLINE)

	# 5. Determine the density of the arrows for plotting
	# # target_num_arrows = 50  # Aim for around 50 arrows in the plot (adjust as needed)
	# # lon_step = max(lons.size // int(np.sqrt(target_num_arrows)), 1)
	# # lat_step = max(lats.size // int(np.sqrt(target_num_arrows)), 1)
	# arrow_density = 10  # Adjust this value to change the density of arrows
	# lon_step = (lons.size // arrow_density) or 1
	# lat_step = (lats.size // arrow_density) or 1
	#
	# # 6. Create a meshgrid for the longitude and latitude coordinates, subsampled for arrow density
	# lon_plot, lat_plot = np.meshgrid(lons[::lon_step], lats[::lat_step])
	# u_plot = u[::lat_step, ::lon_step]
	# v_plot = v[::lat_step, ::lon_step]
	#
	# # 7. Calculate the magnitude of the current for scaling the arrows
	# magnitude = np.sqrt(u_plot ** 2 + v_plot ** 2)

	# 8. Add the vector field plot (quiver) with scaled arrows
	Q = ax.quiver(lons, lats, u, v,
	              scale = 2 / 2.54,  # Adjust this scale factor for arrow length.  The reference unit is 0.5cm.
	              regrid_shape = 20,  # helps with evenly spaced arrows
	              scale_units = 'inches'
	              )

	# 9. Add a scale arrow
	scale_value = 0.5  # m/s
	x_scale = lonlim[1] - 0.4
	y_scale = latlim[0] + 0.2
	ax.quiverkey(Q, x_scale, y_scale, scale_value, f'{scale_value} m/s',
	             labelpos = 'N', coordinates = 'data', color = 'k',
	             fontproperties = {'size': 10})

	# 10. Add title with the date
	plt.title(f'Surface Oceanic Current Velocities on {date.strftime("%d/%m/%Y")}, (72h low-passed and daily '
	          f'averaged)')


# 11. Display the plot
plt.show()


if __name__ == '__main__':
	# # 12. Example usage with dummy data (replace with your actual data)
	# # Define the longitude and latitude vectors
	# lons = np.linspace(-5, -1, 21)  # 21 points between -5 and -1
	# lats = np.linspace(43, 45, 21)  # 21 points between 43 and 45
	#
	# # Create dummy u and v velocity data (21x21 arrays)
	# u = np.zeros((21, 21))
	# v = np.zeros((21, 21))
	#
	# # Create a simple circular flow pattern for the example
	# center_x, center_y = 10, 10
	# for i in range(21):
	#     for j in range(21):
	#         x = i - center_x
	#         y = j - center_y
	#         u[i, j] = -y / 10.0  # Simplified rotational field
	#         v[i, j] = x / 10.0
	#
	# # Create a dummy date
	# date = datetime.datetime(2023, 10, 26)
	#
	# # 13. Call the function to plot the oceanic currents
	# plot_oceanic_currents(u, v, lons, lats, date)

	# ACTUAL TEST WITH REAL DATA
	path2file = r'../data/surface_currents/IBI_data_filt_avg.pkl'
	try:
		with (open(path2file, 'rb') as f):
			data2plot = pickle.load(f)
			print(f"The file '{path2file}' was imported successfully.")
			u = data2plot['u_d_avg']
			v = data2plot['v_d_avg']
			lons = data2plot['lon_ibi']
			lats = data2plot['lat_ibi']
			t = data2plot['t2']

			# Plot
			for d in range(len(t)):
				print(d)
				plot_oceanic_currents(u[:, :, d], v[:, :, d], lons, lats, t[d])
				# Save fig
				plt.savefig(f'../plots/surface_oceanic_currents/ {t[d].strftime("%Y%m%d")}.png', transparent =
				False, bbox_inches = 'tight')
				plt.close()

	except FileNotFoundError:
		print(f"Error: The file '{path2file}' was not found.")
	except Exception as e:
		print(f"An error occurred while importing the file: {e}")
