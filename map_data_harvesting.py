import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import os

from vessel_data_extraction import extract_vessel_data
from Vessel_class import Vessel


# Set up Mercator projection
proj = ccrs.Mercator()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': proj})

###### VESSELS ######
# Define the directory for vessel transect .csv files
directory = r'C:\Users\G to the A\PycharmProjects\Paper\vessels'
# Iteration in this directory
for file in os.scandir(directory):
	if file.is_file():
		# Extract data from .csv file
		data=extract_vessel_data(os.path.join(directory, file))
		# Create object of class vessel
		v=Vessel(data[0],data[1],data[2])
		# plot the transect
		v.plot_transect(a=ax)

###### GLIDER ######

# # Extract time and date information from glider data
# glider_time = pd.to_datetime(glider_df['time'])
#
# # Create a colormap based on time
# cmap = plt.cm.get_cmap('viridis')
# norm = plt.Normalize(vmin=glider_time.min(), vmax=glider_time.max())
#
# # Plot glider path with color-coding
# sc = ax.scatter(glider_df['longitude'], glider_df['latitude'],
#                 c=glider_time, cmap=cmap, norm=norm, transform=ccrs.Geodetic(),
#                 s=10, label='Glider Path')

# Add colorbar
# plt.colorbar(sc, label='Time')

###### CITIES ######
# create a longitude offset so the name and the city point does not overlap
lon_offset=0.02
# Plot Bilbao on the map
ax.plot(-2.92337, 43.25694, 'ko', markersize=6, transform=ccrs.Geodetic())
# Add a label
ax.text(-2.92337+lon_offset, 43.25694, 'Bilbao', transform=ccrs.Geodetic(), fontsize=10, horizontalalignment='left',
        verticalalignment='top')
# Plot Pasaia on the map
ax.plot(-1.92114, 43.32531, 'ko', markersize=6, transform=ccrs.Geodetic())
# Add a label
ax.text(-1.92114+lon_offset, 43.32531, 'Pasaia', transform=ccrs.Geodetic(), fontsize=10, horizontalalignment='left',
        verticalalignment='top')

###### TUNING PLOT ######
# Set map extent to the south-eastern Bay of Biscay
ax.set_extent([-4, -0.5, 43, 45], crs=ccrs.PlateCarree())
# Add coastlines and gridlines
ax.coastlines(resolution='10m') # res can be 10m, 50m or 110m
# Define gridline properties
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
# format coordinates
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# get rid of tick labels on top and right side of the map
gl.top_labels= False
gl.right_labels = False

# Land in light gray
ax.add_feature(cfeature.LAND, facecolor='lightgray')
# Ocean in light blue
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
# Show rivers
ax.add_feature(cfeature.RIVERS)

# Add title and legend
ax.set_title('Vessel Transect and Glider Path in the Bay of Biscay')
ax.legend(loc='lower right')
# Show plot
plt.show()
