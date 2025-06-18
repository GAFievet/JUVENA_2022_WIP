import cartopy.crs as ccrs
import numpy as np
import rasterio

from src import config


def plot_isobaths(ax, bathymetry_file=config.RAW_BATHY, isobath_levels=[-200, -1000],
                  isobath_colors=['blue', 'darkblue']):
	"""
	Plots isobaths on a Cartopy map from a bathymetry file.

	Args:
		ax (cartopy.mpl.geoaxes.GeoAxes): The Cartopy axis on which to plot the isobaths.
		bathymetry_file (str, optional): The path to the bathymetry data file.
										 Defaults to config.RAW_BATHY.
		isobath_levels (list of int/float): A list of depth levels (e.g., [-200, -1000])
													 for which to draw isobaths.
													 Defaults to [-200, -1000].
		isobath_colors (list of str): A list of colors (e.g., ['blue', 'darkblue'])
												corresponding to each isobath_level.
												Must have the same length as isobath_levels.
												Defaults to ['blue', 'darkblue'].
	"""

	# Basic validation: ensure number of levels matches number of colors
	if len(isobath_levels) != len(isobath_colors):
		raise ValueError("The number of isobath levels must match the number of isobath colors.")

	try:
		# Open the bathymetry GeoTIFF file
		with rasterio.open(bathymetry_file) as src:
			# Read the bathymetry data (first band)
			bathymetry_data = src.read(1)

			# Get 1D longitude and latitude arrays
			# Use src.bounds and src.width/height for creating 1D coordinate arrays suitable for contour(X_1D, Y_1D,
			# Z_2D)
			# This ensures lons has length = src.width (cols) and lats has length = src.height (rows)
			lons = np.linspace(src.bounds.left, src.bounds.right, src.width)
			lats = np.linspace(src.bounds.bottom, src.bounds.top, src.height)

			bathymetry_data = np.flipud(bathymetry_data)

		# Plot the isobaths
		for i, level in enumerate(isobath_levels):
			contour = ax.contour(lons, lats, bathymetry_data, levels = [level],
			                     colors = [isobath_colors[i]], linestyles = '--', linewidths = 0.5,
			                     transform = ccrs.PlateCarree(), zorder=0)
			# Add labels to the isobaths (optional, but useful for identification)
			# ax.clabel(contour, inline = True, fontsize = 2, fmt = f'{level}m', inline_spacing=5)

	except FileNotFoundError:
		print(f"Error: Bathymetry file '{bathymetry_file}' not found.")
		print("Please ensure the path is correct and the file exists.")
	except Exception as e:
		print(f"An error occurred while plotting the isobaths: {e}")
