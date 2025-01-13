import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import os
import pickle

from Glider_class import Glider
from vessel_data_extraction import extract_vessel_data
from Vessel_class import Vessel

# Set up Mercator projection
proj = ccrs.Mercator()

# Create a figure and axis
fig, ax = plt.subplots(figsize = (7, 7), subplot_kw = {'projection': proj})

###### VESSELS ######
# Define the directory for vessel transect .csv files
directory = r'C:\Users\G to the A\PycharmProjects\Paper\vessels'
all_files = os.listdir(directory)
pkl_files = [f for f in all_files if f.endswith('.pkl')]
for file in pkl_files:
	# Get vessel data
	with open(os.path.join(directory, file), 'rb') as f:
		vessel_mat = pickle.load(f)
	# Create object of class vessel
	v = Vessel(vessel_mat[0], vessel_mat[1], vessel_mat[2])
	# plot the transect
	v.plot_transect(a = ax)

###### GLIDER ######

# Load the list from the extraction_file
glider_extract = r'C:\Users\G to the A\PycharmProjects\Paper\glider\glider_GPS.pkl'
with open(glider_extract, 'rb') as f:
	glider_GPS = pickle.load(f)

glider = Glider(glider_GPS[0], glider_GPS[1], glider_GPS[2])
glider.plot_transect(fig, ax)

###### CITIES ######
# create a longitude offset so the name and the city point does not overlap
offset = 0.02
# Plot Bilbao on the map
ax.plot(-2.92337, 43.25694, 'ko', markersize = 6, transform = ccrs.Geodetic())
# Add a label
ax.text(-2.92337 + offset, 43.25694, 'Bilbao', transform = ccrs.Geodetic(), fontsize = 10,
        horizontalalignment = 'left',
        verticalalignment = 'top')
# Plot Pasaia on the map
ax.plot(-1.92114, 43.32531, 'ko', markersize = 6, transform = ccrs.Geodetic())
# Add a label
ax.text(-1.92114 - offset, 43.32531 - 1.5 * offset, 'Pasaia', transform = ccrs.Geodetic(), fontsize = 10,
        horizontalalignment = 'right',
        verticalalignment = 'top')

###### TUNING PLOT ######
# Set map extent to the south-eastern Bay of Biscay
ax.set_extent([-3.5, -1.8, 43.2, 44.35], crs = ccrs.PlateCarree())
# Add coastlines and gridlines
ax.coastlines(resolution = '10m')  # res can be 10m, 50m or 110m
# Define gridline properties
gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color = 'gray', alpha = 0.5,
                  linestyle = '--')
# format coordinates
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# get rid of tick labels on top and right side of the map
gl.top_labels = False
gl.right_labels = False

# Land in light gray
ax.add_feature(cfeature.LAND, facecolor = 'lightgray')
# Ocean in light blue
ax.add_feature(cfeature.OCEAN, facecolor = 'lightblue')
# Show rivers
ax.add_feature(cfeature.RIVERS)
# Borders
ax.add_feature(cfeature.BORDERS, linestyle = ':')

# Add title and legend
# ax.set_title('Sampling effort during the JUVENA 2022 survey')
ax.legend(loc = 'upper right')
# Save fig
plt.savefig(r'C:\Users\G to the A\PycharmProjects\Paper\plots\sampling_effort.png', transparent = True)
# Show plot
plt.show()
