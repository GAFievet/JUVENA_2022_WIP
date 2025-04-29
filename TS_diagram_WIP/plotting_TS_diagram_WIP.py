from datetime import datetime
import matplotlib.pyplot as plt
import gsw
import numpy as np
import pandas as pd  # For reading CSV files and handling dataframes
import scipy.io  # For loading MAT files

import TS_depth
from datetime_formating import matlab2python

# --- Step 1: Load and prepare plotting ---
# --- Load glider & CTD data ---
glider_data = scipy.io.loadmat(r'../data/glider/CTD/PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat')
conductivity = np.squeeze(glider_data['conductivity'])
depth = np.squeeze(glider_data['depth'])
latitude = np.squeeze(glider_data['latitude'])
longitude = np.squeeze(glider_data['longitude'])
pressure = np.squeeze(glider_data['pressure'])
salinity = np.squeeze(glider_data['salinity'])
temperature = np.squeeze(glider_data['temperature'])
time = [matlab2python(date) for date in np.squeeze(glider_data['time'])]

# --- Load Anchovy data Work In Progress ---
ancho_data = scipy.io.loadmat("deepest_ancho_start_depth.mat")
deepest_ancho = ancho_data["deepest_ancho"]


# --- Derive density and potential temperature ---
density = gsw.dens(salinity, temperature, pressure)
pdens = gsw.pden(salinity, temperature, pressure, 0)
ptemp = gsw.ptmp(salinity, temperature, pressure, 0)

# --- Span of the mission to plot ---
t1 = datetime.strptime("01/10/2022 00:00:00", "%d/%m/%Y %H:%M:%S")
t2 = datetime.strptime("06/10/2022 23:59:59", "%d/%m/%Y %H:%M:%S")

# --- FILTER DATES ---
i1 = np.where((time > t1) & (time < t2))[0][0]
i2 = np.where((time > t1) & (time < t2))[0][-1]
fig =plt.figure(figsize=(6,8))
ax1=fig.add_subplot(1,2,1)

# Plot TS-depth diagram
TSdepth=TS_depth(ax1,pressure,latitude,time,salinity,ptemp)

# --- Step 3: 2D SCATTER TS-DENSITY/ACOUSTIC ---
# Read anchovy detection file
Sv_ancho_mission = pd.read_csv("all_anchovy_data.csv")
# Extract time, depth and acoustic volumetric backscattering coeficient (dB)
time_Sv = Sv_ancho_mission['Time'].values
depth_Sv = Sv_ancho_mission['Depth_start'].values
backscatter = Sv_ancho_mission['Sv'].values

# Plot TS-backscattering diagram
# TSbackscatter=TS_depth(ax1,pressure,latitude,time,salinity,ptemp,backscatter)


# generating background density contours:

# plotting background density contours:

# plotting scatter plot of theta and s:
ax2=fig.add_subplot(1,2,2)
ax[1].scatter(s[idx_depth], theta[idx_depth], c=-dep[idx_depth], s=4, marker='o',  cmap='gray') # scatter(s(idx_depth),theta(idx_depth),4,-dep(idx_depth),"MarkerFaceColor",[0.5 0.5 0.5],"MarkerEdgeColor","none");
scatter_sv = ax[1].scatter(s[idx_depth], theta[idx_depth], c=Sv_matQ[idx_depth], s=4, cmap='jet') # scatter(s(idx_depth),theta(idx_depth),4,Sv_matQ(idx_depth),'filled');
plt.colorbar(scatter_sv, ax=ax[1], label='dB', orientation='vertical', extend='both') # a = colorbar; a.Label.String = 'dB';
ax[1].set_title(title_str) # title(title_str);

print("Step 3 conversion to Python complete")

