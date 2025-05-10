from datetime import datetime

import gsw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io  # For loading MAT files

from TS_depth import TS_depth
from TS_diagram_WIP.TS_acoustic_WIP import ts_backscatter
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
# ancho_data = scipy.io.loadmat("deepest_ancho_start_depth.mat")
# deepest_ancho = ancho_data["deepest_ancho"]

# --- Derive density and potential temperature ---
density = gsw.rho(salinity, temperature, pressure)
pdens = gsw.density.sigma1(salinity, temperature)
ptemp = gsw.pt_from_t(salinity, temperature, pressure, 0)

# --- Span of the mission to plot ---
t1 = datetime.strptime("23/09/2022 00:00:00", "%d/%m/%Y %H:%M:%S")
t2 = datetime.strptime("06/10/2022 23:59:59", "%d/%m/%Y %H:%M:%S")

# --- FILTER CTD DATA TO PLOT ONLY THE CHOSEN PERIOD  ---
# Get idx of start and end
i1 = np.where((time > t1) & (time < t2))[0][0]
i2 = np.where((time > t1) & (time < t2))[0][-1]
#  Apply to all datas
pressure = pressure[i1:i2]
latitude = latitude[i1:i2]
time = time[i1:i2]
salinity = salinity[i1:i2]
ptemp = ptemp[i1:i2]
# Create fig
fig = plt.figure(figsize = (6, 8))
# Create 1st set of axis
ax1 = fig.add_subplot(1, 2, 1)

# Plot TS-depth diagram
TSdepth = TS_depth(ax1, pressure, latitude, time, salinity, ptemp)

# --- Step 3: 2D SCATTER TS-DENSITY/ACOUSTIC ---
#  Create 2nd set of axis
ax2 = fig.add_subplot(1, 2, 2)
# Read anchovy detection file
acoustic_data = pd.read_csv("all_anchovy_data.csv")
acoustic_data = acoustic_data.sort_values(by = "Time")  # Ensure the df is sorted along time
# Filter the period of time
acoustic_time = [matlab2python(t) for t in acoustic_data["Time"]]
# Get idx of start and end
acoustic_i1 = np.where((acoustic_time > t1) & (acoustic_time < t2))[0][0]
acoustic_i2 = np.where((acoustic_time > t1) & (acoustic_time < t2))[0][-1]
# Filter dataframe
acoustic_data = acoustic_data.loc[acoustic_i1:acoustic_i2]
# Plot TS-backscattering diagram
TSbackscatter = ts_backscatter(ax2, pressure, latitude, time, salinity, ptemp, acoustic_data)
