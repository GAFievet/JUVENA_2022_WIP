import os

# Set the GDAL_DATA environment variable
# This is a safety measure if GDAL_DATA is not consistently recognized by your Conda environment
os.environ['GDAL_DATA'] = r'C:\Users\G to the A\anaconda3\envs\JUVENA2022\Library\share\gdal'
# print(f"DEBUG (plot_utils): GDAL_DATA is set to: {os.environ.get('GDAL_DATA')}")

import geopandas
from shapely.geometry import LineString, Polygon
from plot_utils import plot_isobaths
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
from src import config

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
# Set map extent
ax1.set_extent(
	[config.BAY_OF_BISCAY['min_lon'],
	 config.BAY_OF_BISCAY['max_lon'],
	 config.BAY_OF_BISCAY['min_lat'],
	 config.BAY_OF_BISCAY['max_lat']], crs = ccrs.PlateCarree())
# endregion

# region ###### CITIES ######
# create a longitude offset so the name and the city point does not overlap
offset = 0.05
# Plot Bilbao on the map
ax1.plot(-2.92337, 43.25694, 'ko', markersize = 3, transform = ccrs.Geodetic())
# Add a label
ax1.text(-2.92337 + offset, 43.25694 - 2 * offset, 'Bilbao', transform = ccrs.Geodetic(), fontsize = 4,
         horizontalalignment = 'left',
         verticalalignment = 'top')
# Plot Pasaia on the map
ax1.plot(-1.92114, 43.32531, 'ko', markersize = 3, transform = ccrs.Geodetic())
# Add a label
ax1.text(-1.92114 + 2 * offset, 43.32531 - 1 * offset, 'Pasaia', transform = ccrs.Geodetic(), fontsize = 4,
         horizontalalignment = 'right',
         verticalalignment = 'top')
# Plot Nantes on the map
ax1.plot(-1.55, 47.216671, 'ko', markersize = 3, transform = ccrs.Geodetic())
# Add a label
ax1.text(-1.55 - 2 * offset, 47.216671 - 2 * offset, 'Nantes', transform = ccrs.Geodetic(), fontsize = 4,
         horizontalalignment = 'left',
         verticalalignment = 'top')
# Plot Gijon on the map
ax1.plot(-5.66192640, 43.54526080, 'ko', markersize = 3, transform = ccrs.Geodetic())
# Add a label
ax1.text(-5.66192640 - offset, 43.54526080 - 2 * offset, 'Gijón', transform = ccrs.Geodetic(), fontsize = 4,
         horizontalalignment = 'left',
         verticalalignment = 'top')
# endregion

# region ###### ISOBATHS ######
# Call the function to plot the isobaths and run default args
plot_isobaths(ax1)
# endregion

# region ###### GEODATAFRAMES FOR Ramon Margalef & Emma Bardan ######
df_aa = pd.read_csv(config.RAW_RADIALS_AA, sep = '\t')
gdf_aa = geopandas.GeoDataFrame(
	df_aa, geometry = df_aa.apply(
		lambda row: LineString([(row['long_ini'], row['lat_ini']), (row['long_fin'], row['lat_fin'])]), axis = 1),
	crs = "EPSG:4326")

df_eb = pd.read_csv(config.RAW_RADIALS_EB, sep = '\t')
gdf_eb = geopandas.GeoDataFrame(
	df_eb, geometry = df_eb.apply(
		lambda row: LineString([(row['long_ini'], row['lat_ini']), (row['long_fin'], row['lat_fin'])]), axis = 1),
	crs = "EPSG:4326")
# endregion

# region ###### PLOT TRANSECTS ######
gdf_eb.plot(ax = ax1, color = '#8AB8F0', linewidth = 1, label = 'R/V Emma Bardan', transform = ccrs.PlateCarree(),
            zorder = 10)
gdf_aa.plot(ax = ax1, color = '#F08A8A', linewidth = 1, label = 'R/V Ramón Margalef', transform = ccrs.PlateCarree(),
            zorder = 10)

# Add labels for Radiales EB
for idx, row in gdf_eb.iterrows():
	ax1.text(row['long_ini'], row['lat_ini'], row['Radial'], color = '#6A9ACB', fontsize = 4.5,
	         transform = ccrs.PlateCarree(), ha = 'right', va = 'bottom', zorder = 11)

# Add labels for Radiales AA
for idx, row in gdf_aa.iterrows():
	ax1.text(row['long_ini'], row['lat_ini'], row['Radial'], color = '#F08A8A', fontsize = 4.5,
	         transform = ccrs.PlateCarree(), ha = 'right', va = 'bottom', zorder = 11)
# endregion

# region ###### FRAME V8 ######
frame_polygon = Polygon([(config.BAY_OF_BISCAY_SE_BOUNDS['min_lon'], config.BAY_OF_BISCAY_SE_BOUNDS['min_lat']),
                         (config.BAY_OF_BISCAY_SE_BOUNDS['min_lon'], config.BAY_OF_BISCAY_SE_BOUNDS['max_lat']),
                         (config.BAY_OF_BISCAY_SE_BOUNDS['max_lon'], config.BAY_OF_BISCAY_SE_BOUNDS['max_lat']),
                         (config.BAY_OF_BISCAY_SE_BOUNDS['max_lon'], config.BAY_OF_BISCAY_SE_BOUNDS['min_lat'])])

# Créer un GeoDataFrame temporaire pour le cadre
gdf_frame = geopandas.GeoDataFrame(geometry = [frame_polygon], crs = "EPSG:4326")

# Tracer le cadre en pointillé
gdf_frame.plot(ax = ax1, facecolor = 'none', edgecolor = 'black', linewidth = 0.5, linestyle = '--',
               transform = ccrs.PlateCarree(), zorder = 12)
# endregion

# Add a legend
ax1.legend(loc = 'upper left', fontsize = 5)

# Save fig
plt.savefig(config.JUVENA2022_OVERVIEW, transparent = True, dpi = config.DEFAULT_PLOT_DPI, bbox_inches = 'tight')

# Show plot
# plt.show()
