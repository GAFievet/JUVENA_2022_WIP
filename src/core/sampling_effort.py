import glob
import os

# Set the GDAL_DATA environment variable
# This is a safety measure if GDAL_DATA is not consistently recognized by your Conda environment
os.environ['GDAL_DATA'] = r'C:\Users\G to the A\anaconda3\envs\JUVENA2022\Library\share\gdal'
# print(f"DEBUG (plot_utils): GDAL_DATA is set to: {os.environ.get('GDAL_DATA')}")
import pickle
from datetime import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot_utils import plot_isobaths
from src import config
from src.glider_processing.Glider_class import Glider
from src.vessel_echo_processing.Vessel_echo_class import Vessel_echo
from src.vessel_fishing_processing.Vessel_fishing_class import Vessel_fishing

# from cartopy.feature import NaturalEarthFeature

# Set up Mercator projection
proj = ccrs.Mercator()

# Create a figure and axis
fig, ax1 = plt.subplots(figsize = (10, 5), subplot_kw = {'projection': proj})

# region ###### BACKGROUND ######
# Land in light gray
ax1.add_feature(cfeature.LAND, facecolor = 'lightgray')
# Ocean in light blue
ax1.add_feature(cfeature.OCEAN, facecolor = 'white')
# Show rivers
ax1.add_feature(cfeature.RIVERS)
# Borders
ax1.add_feature(cfeature.BORDERS, linestyle = ':')
# Add coastlines and gridlines
ax1.coastlines(resolution = '10m')  # res can be 10m, 50m or 110m
# endregion

# region ###### CITIES ######
# create a longitude offset so the name and the city point does not overlap
offset = 0.02
# Plot Bilbao on the map
ax1.plot(-2.92337, 43.25694, 'ko', markersize = 6, transform = ccrs.Geodetic())
# Add a label
ax1.text(-2.92337 + offset, 43.25694, 'Bilbao', transform = ccrs.Geodetic(), fontsize = 10,
         horizontalalignment = 'left',
         verticalalignment = 'top')
# Plot Pasaia on the map
ax1.plot(-1.92114, 43.32531, 'ko', markersize = 6, transform = ccrs.Geodetic())
# Add a label
ax1.text(-1.92114 - offset, 43.32531 - 1.5 * offset, 'Pasaia', transform = ccrs.Geodetic(), fontsize = 10,
         horizontalalignment = 'right',
         verticalalignment = 'top')
# endregion

# region ###### ISOBATHS ######
# Call the function to plot the isobaths and run default args
plot_isobaths(ax1)
# endregion

# region ###### VESSELS ECHO ######
# Define the directory for vessel echosounding transect files
directory_echo = config.VESSEL_ECHO
echo_PKLs = glob.glob(os.path.join(directory_echo, '*2022*.pkl'))
# Adjust longitudinal spreading of transects
longitude_shifts = np.linspace(-0.025, 0.025, len(echo_PKLs)).tolist()
for file in echo_PKLs:
	# Get vessel data
	with open(file, 'rb') as f:
		vessel_mat = pickle.load(f)
	# Create object of class vessel_echo
	v_e = Vessel_echo(vessel_mat[0], vessel_mat[1], vessel_mat[2])
	# plot the transect
	v_e.plot_transect(ax1, longitude_shifts[0])
	longitude_shifts.pop(0)
# endregion

# region ###### VESSEL FISHING ######
# Define the directory for vessel echosounding transect files
directory_haul = config.VESSEL_HAULS
haul_PKLs = glob.glob(os.path.join(directory_haul, 'haul*.pkl'))
# Adjust longitudinal spreading of transects
longitude_shifts = np.linspace(-0.025, 0.025, len(haul_PKLs)).tolist()
# Create new axis for piecharts
for i, file in enumerate(haul_PKLs):
	# Get vessel data
	with open(file, 'rb') as f:
		vessel_dict = pickle.load(f)
	# Create object of class vessel_fishing
	v_f = Vessel_fishing(vessel_dict['loc_i'], vessel_dict['loc_f'], vessel_dict['date'], vessel_dict['species'],
	                     vessel_dict['masses'], vessel_dict['color palette'], vessel_dict['transect'])
	# Plot the trawl
	v_f.plot_transect(ax1, longitude_shifts[0])
	# # Plot associated pie chart for species fished
	# ax2 = inset_axes(ax1, width = "40%", height = "40%", loc = 2, bbox_to_anchor = (-0.35, 0.6 - 0.2 * i, 0.4, 0.4),
	#                  bbox_transform = ax1.transAxes)
	# if v_f.orientation == 'v':
	# 	vessel_loc = [v_f.lons[0] + longitude_shifts[0], v_f.lats[0]]
	# else:
	# 	vessel_loc = [v_f.lons[1] + longitude_shifts[0], v_f.lats[1]]
	# # v_f.abundance_pie_chart(ax1, ax2, vessel_loc)
	longitude_shifts.pop(0)
# endregion

# region ###### GLIDER PATH ######
glider_GPS_df = pd.read_csv(config.RAW_GPS)
GPS_dates = glider_GPS_df['GPS_date'].tolist()
GPS_dates = [datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S") for date_string in GPS_dates]
GPS_lons = glider_GPS_df['Longitude'].tolist()
GPS_lats = glider_GPS_df['Latitude'].tolist()

glider = Glider(GPS_lons, GPS_lats, GPS_dates)
glider.plot_transect(fig, ax1)
# endregion

# region ###### TUNING PLOT ######
# Set map extent to the south-eastern Bay of Biscay
ax1.set_extent(
	[config.BAY_OF_BISCAY_SE_BOUNDS['min_lon'],
	 config.BAY_OF_BISCAY_SE_BOUNDS['max_lon'],
	 config.BAY_OF_BISCAY_SE_BOUNDS['min_lat'],
	 config.BAY_OF_BISCAY_SE_BOUNDS['max_lat']], crs = ccrs.PlateCarree())

# Add legend
# ax1.legend(bbox_to_anchor = (-0.05, 1), loc = 'upper right', borderaxespad = 0., ncol = 1)
# Adjust the left margin to make space for the legend
# plt.subplots_adjust(left = 0.25)
ax1.legend(bbox_to_anchor = (0.7, -0.4), loc = 'lower center', borderaxespad = 0., ncol = 3)
plt.subplots_adjust(bottom = 0.2)
# endregion

#region Define gridline properties
# gl = ax1.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color = 'gray', alpha = 0.5,
#                    linestyle = '--')
# format coordinates
# gl.xformatter = LONGITUDE_FORMATTER
# gl.yformatter = LATITUDE_FORMATTER
# get rid of tick labels on top and right side of the map
# gl.top_labels = False
# gl.right_labels = False
# endregion

# Save fig
plt.savefig(config.SAMPLING_EFFORTS, transparent = True, dpi = config.DEFAULT_PLOT_DPI, bbox_inches = 'tight')
# Show plot
# plt.show()
