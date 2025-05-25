from datetime import datetime

import gsw
import matplotlib

matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io as sio  # For loading MAT files
from find_time_index import find_time_indices
from TS_depth import TS_depth
from src.TS_diagram_WIP.TS_acoustic import ts_backscatter
from src.core.datetime_formating import matlab2python

# --- Step 1: Load and prepare plotting ---
# --- Load glider & CTD data ---
path_CTD = r'../../data/glider/CTD/PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat'
try:
	glider_data = sio.loadmat(path_CTD)
	# Extract data
	conductivity = np.squeeze(glider_data['conductivity'])
	depth = np.squeeze(glider_data['depth'])
	latitude = np.squeeze(glider_data['latitude'])
	longitude = np.squeeze(glider_data['longitude'])
	pressure = np.squeeze(glider_data['pressure'])
	salinity = np.squeeze(glider_data['salinity'])
	temperature = np.squeeze(glider_data['temperature'])
	time = [matlab2python(date) for date in np.squeeze(glider_data['time'])]

except FileNotFoundError:
	print(f"Erreur : The file '{path_CTD}' could not be found.")
except Exception as e:
	print(f"An error occured while reading the file : {e}")
# --- Load Anchovy data Work In Progress ---
# ancho_data = scipy.io.loadmat("deepest_ancho_start_depth.mat")
# deepest_ancho = ancho_data["deepest_ancho"]

# --- Derive absolute salinity, conservative temperature, density and potential density anomaly ---
"""
While EOS-80 involved Practical Salinity and potential temperature, TEOS-10 involves absolute salinity and 
conservative temperature
"""
# Expand latitude and longitude to match salinity and pressure dim
longitude_extended = np.repeat(longitude, salinity.shape[1]).reshape(salinity.shape)
latitude_extended = np.repeat(latitude, salinity.shape[1]).reshape(salinity.shape)

# 1. Calculate Absolute Salinity from Practical Salinity
abs_sal = gsw.SA_from_SP(salinity, pressure, longitude_extended, latitude_extended)

# 2. Calculate Conservative Temperature from in-situ temperature
cons_temperature = gsw.CT_from_t(abs_sal, temperature, pressure)

# 3. Calculate in-situ density (kg/m^3) 
density = gsw.rho(abs_sal, cons_temperature, pressure)

# 4. Calculate potential density anomaly (kg/m^3) referenced to pressure = 0 dbar
pdens = gsw.rho(abs_sal, gsw.CT_from_pt(abs_sal, cons_temperature), 0) - 1000

# # 5. Calculate potential temperature (degrees Celsius) referenced to pressure = 0 dbar
# cons_temp = gsw.pt_from_CT(abs_sal, cons_temperature)

# --- Span of the mission to plot ---
t1 = datetime.strptime("23/09/2022 00:00:00", "%d/%m/%Y %H:%M:%S")
t2 = datetime.strptime("06/10/2022 23:59:59", "%d/%m/%Y %H:%M:%S")

# --- FILTER CTD DATA TO PLOT ONLY THE CHOSEN PERIOD  ---
# Get idx of start and end
i1,i2=find_time_indices(time,t1,t2)
if i1!=-1 and i2!=-1:
	#  Apply to all datas
	conductivity = conductivity[i1:i2]
	latitude = latitude[i1:i2]
	longitude = longitude[i1:i2]
	pressure = pressure[i1:i2]
	abs_sal = abs_sal[i1:i2]
	temperature = temperature[i1:i2]
	time = time[i1:i2]
	cons_temperature = cons_temperature[i1:i2]
	pdens = pdens[i1:i2]
	density = density[i1:i2]

# Create fig
fig = plt.figure(figsize = (10, 5))
# Create 1st set of axis
ax1 = fig.add_subplot(1, 2, 1)

# Plot TS-depth diagram
TSdepth = TS_depth(ax1 ,time, pressure, latitude_extended, abs_sal, cons_temperature)

# --- Step 3: 2D SCATTER TS-DENSITY/ACOUSTIC ---
#  Create 2nd set of axis
ax2 = fig.add_subplot(1, 2, 2)
# Read anchovy detection file
acoustic_data = pd.read_csv("../../data/glider/echosounder/all_anchovy_data.csv")
acoustic_data = acoustic_data.sort_values(by = "Time")  # Ensure the df is sorted along time
# Filter the period of time
acoustic_time = [matlab2python(t) for t in acoustic_data["Time"]]
# Get idx of start and end
i1,i2=find_time_indices(time,t1,t2)
if i1!=-1 and i2!=-1:
	# Filter dataframe
	acoustic_data = acoustic_data.loc[i1:i2]
# Plot TS-backscattering diagram
TSbackscatter = ts_backscatter(ax2, time, pressure, latitude_extended, abs_sal, cons_temperature, acoustic_data)

plt.show()