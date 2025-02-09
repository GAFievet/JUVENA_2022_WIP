import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import os
import pickle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from Glider_class import Glider
from Vessel_echo_class import Vessel_echo
from Vessel_fishing_class import Vessel_fishing

# Set up Mercator projection
proj = ccrs.Mercator()

# Create a figure and axis
fig, ax1 = plt.subplots(figsize = (10, 5), subplot_kw = {'projection': proj})

# Adjust longitudinal spreading of transects
# Find how many transects are to plot
n = 0
for root, dirs, files in os.walk(r'C:\Users\G to the A\PycharmProjects\Paper'):
	for file in files:
		if file.endswith(".pkl") and file not in ('color_palette.pkl', 'glider_GPS.pkl','CTD.pkl'):
			n += 1

# Calculate longitude shifts
longitude_shifts = np.linspace(-0.025, 0.025, n).tolist()

###### VESSELS ECHO ######
# Define the directory for vessel echosounding transect files
directory = r'C:\Users\G to the A\PycharmProjects\Paper\vessels_echo'
all_files = os.listdir(directory)
pkl_files = [f for f in all_files if f.endswith('.pkl')]
for file in pkl_files:
	# Get vessel data
	with open(os.path.join(directory, file), 'rb') as f:
		vessel_mat = pickle.load(f)
	# Create object of class vessel_echo
	v_e = Vessel_echo(vessel_mat[0], vessel_mat[1], vessel_mat[2])
	# plot the transect
	v_e.plot_transect(ax1, longitude_shifts[0])
	longitude_shifts.pop(0)

###### VESSEL FISHING ######
# Define the directory for vessel echosounding transect files
directory = r'C:\Users\G to the A\PycharmProjects\Paper\vessel_fishing'
all_files = os.listdir(directory)
pkl_files = [f for f in all_files if f.endswith('.pkl') and f != 'color_palette.pkl']
# Create new axis for piecharts
for i, file in enumerate(pkl_files):
	# Get vessel data
	with open(os.path.join(directory, file), 'rb') as f:
		vessel_dict = pickle.load(f)
	# Create object of class vessel_fishing
	v_f = Vessel_fishing(vessel_dict['loc_i'], vessel_dict['loc_f'], vessel_dict['date'], vessel_dict['species'],
	                     vessel_dict['masses'], vessel_dict['color palette'])
	# Plot the trawl
	v_f.plot_transect(ax1, longitude_shifts[0])
	# Plot associated pie chart for species fished
	ax2 = inset_axes(ax1, width = "40%", height = "40%", loc = 2, bbox_to_anchor = (-0.35, 0.6 - 0.2 * i, 0.4, 0.4),
	                 bbox_transform = ax1.transAxes)
	if v_f.orientation == 'v':
		vessel_loc=[v_f.lons[0] + longitude_shifts[0], v_f.lats[0]]
	else:
		vessel_loc = [v_f.lons[1] + longitude_shifts[0], v_f.lats[1]]
	v_f.abundance_pie_chart(ax1, ax2,vessel_loc)
	longitude_shifts.pop(0)

###### GLIDER ######

# Load the list from the extraction_file
glider_extract = r'C:\Users\G to the A\PycharmProjects\Paper\glider\glider_GPS.pkl'
with open(glider_extract, 'rb') as f:
	glider_GPS = pickle.load(f)

glider = Glider(glider_GPS[0], glider_GPS[1], glider_GPS[2])
glider.plot_transect(fig, ax1)

###### CITIES ######
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

###### TUNING PLOT ######
# Set map extent to the south-eastern Bay of Biscay
ax1.set_extent([-3.5, -1.8, 43.2, 44.35], crs = ccrs.PlateCarree())
# Add coastlines and gridlines
ax1.coastlines(resolution = '10m')  # res can be 10m, 50m or 110m
# Define gridline properties
gl = ax1.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color = 'gray', alpha = 0.5,
                   linestyle = '--')
# format coordinates
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# get rid of tick labels on top and right side of the map
gl.top_labels = False
gl.right_labels = False

# Land in light gray
ax1.add_feature(cfeature.LAND, facecolor = 'lightgray')
# Ocean in light blue
ax1.add_feature(cfeature.OCEAN, facecolor = 'lightblue')
# Show rivers
ax1.add_feature(cfeature.RIVERS)
# Borders
ax1.add_feature(cfeature.BORDERS, linestyle = ':')

# Add title and legend
# ax1.set_title('Sampling effort during the JUVENA 2022 survey')
ax1.legend(loc = 'upper right')
# Save fig
plt.savefig(r'C:\Users\G to the A\PycharmProjects\Paper\plots\sampling_effort.png', transparent = True,
            bbox_inches = 'tight')
# Show plot
plt.show()
