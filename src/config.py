# src/config.py

import os
from datetime import datetime

# --- Project Base Directory ---
# This ensures that all paths are relative to the project root,
# making the project portable across different machines.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Data Paths ---
# Centralized locations for raw (input), processed data, and outputs.
# "Raw" here refers to the input data for THIS project, which might be
# output from Echoview or other pre-processing steps.
INPUT_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')  # Renamed from RAW_DATA_DIR for clarity
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# --- INPUT Data Specific Paths ---
# These are the *inputs* to your project, which are already pre-processed outputs
# from acoustic software like Echoview.

# BoB Bathymetry 15 sec arc
RAW_BATHY= os.path.join(INPUT_DATA_DIR, 'gebco_2024_n48.0_s43.0_w-8.0_e-1.0.tif')
# SURFACE CURRENTS
RAW_SURFACE_CURRENT = os.path.join(INPUT_DATA_DIR, 'surface_currents', 'IBI_data.mat')
# VESSEL ACOUSTIC
RAW_VESSEL_ECHO = os.path.join(INPUT_DATA_DIR, 'vessel', 'vessel_echo')
# VESSEL FISHING
RAW_VESSEL_FISHING = os.path.join(INPUT_DATA_DIR, 'vessel', 'vessel_fishing','Selected_trawls_around_intensive_transect.xlsx')
# VESSEL JUVENA 2022 OVERVIEW
# Ramon Margalef (BIG)
RAW_RADIALS_AA=os.path.join(INPUT_DATA_DIR, 'vessel','radialesAA.txt')
# Emma Bardan (SMALL)
RAW_RADIALS_EB=os.path.join(INPUT_DATA_DIR, 'vessel','radialesEB.txt')

###  GLIDER  ###
# RAW GLIDER DIR
RAW_GLIDER_DIR = os.path.join(INPUT_DATA_DIR, 'glider')
# MLD FILTERED
RAW_MLD_FILTERED = os.path.join(RAW_GLIDER_DIR, 'CTD', 'MLD_filtered.mat')
# CTD .MAT
RAW_CTD = os.path.join(RAW_GLIDER_DIR, 'CTD', 'PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat')
# RAW GPS
RAW_GPS = os.path.join(RAW_GLIDER_DIR, 'glider.gps.csv')
# RAW PATH BATHY
RAW_GLIDER_BATHY=os.path.join(RAW_GLIDER_DIR, 'floor_depth_profile_2309_0610.mat')

# --- Output File Names (for processed data, visualization-ready) ---
# SURFACE CURRENTS
# Filtered currents
FILT_SURFACE_CURRENTS = os.path.join(PROCESSED_DATA_DIR, 'surface_currents', 'IBI_data_filt', '.pkl')
# Filtered and daily averaged currents
AVG_FILT_SURFACE_CURRENTS = os.path.join(PROCESSED_DATA_DIR, 'surface_currents', 'IBI_data_filt_avg', '.pkl')
# VESSEL ACOUSTIC
VESSEL_ECHO = os.path.join(PROCESSED_DATA_DIR, 'vessel_echo')
# VESSEL FISHING
# Hauls data
VESSEL_HAULS = os.path.join(PROCESSED_DATA_DIR, 'vessel_fishing')
# Colour palette assigning a color per fish species
VESSEL_COLOR_PALETTE = os.path.join(PROCESSED_DATA_DIR, 'vessel_fishing','color_palette.pkl')
###  GLIDER  ###
# PROCESSED GLIDER DIR
PROCESSED_GLIDER_DIR = os.path.join(PROCESSED_DATA_DIR, 'glider')
# DAILY GPS
DAILY_GLIDER_GPS = os.path.join(PROCESSED_GLIDER_DIR, 'Daily_GPS', 'Glider_*.gps.csv')
# ALL ANCHOVY DATA GLIDER ECHO
PROCESSED_GLIDER_ANCHO = os.path.join(PROCESSED_GLIDER_DIR, 'echosounder', 'Juvenile_Anchovy_datasets_Sv_lin.csv')

# --- Plot File Names (.png) ---
# SURFACE OCEANIC CURRENTS MAPS
SURFACE_OCEANIC_CURRENTS_MAPS = os.path.join(PLOTS_DIR, 'surface_oceanic_currents')
SAMPLING_EFFORTS = os.path.join(PLOTS_DIR, 'map_sampling_effort.png')
JUVENA2022_OVERVIEW=os.path.join(PLOTS_DIR, 'map_JUVENA2022_overview.png')
SURVEY_PROFILE=os.path.join(PLOTS_DIR, 'survey_profile.png')
# --- Geographic and Temporal Bounds ---
# Define the regions of interest for the Southeast Bay of Biscay
BAY_OF_BISCAY={
	'min_lat': 43,
	'max_lat': 48,
	'min_lon': -8,
	'max_lon': -1
}
# Adjust these coordinates as precisely as needed for your study area
BAY_OF_BISCAY_SE_BOUNDS = {
	'min_lat': 43.2,
	'max_lat': 44.35,
	'min_lon': -3.5,
	'max_lon': -1.8
}

# Define the typical survey period or analysis window
SURVEY_START_DATE = datetime(2022, 9, 23)  # 23 Sept. 2022
SURVEY_END_DATE = datetime(2022, 10, 6)  # 06 Oct. 2022

# --- Echosounder (Contextual) Parameters ---
# These parameters might still be relevant for context or advanced plotting,
# even if you're not doing raw processing. Keep them if you use them in plots/analysis descriptions.
ECHOSOUNDER_FREQUENCY_KHZ = 200  # Example: 200 kHz
TRANSDUCER_BEAM_WIDTH_DEG = 7.0  # Example: 7 degrees
# PULSE_LENGTH_MS = 0.5         # Might not be needed if not raw processing
# ABSORPTION_COEFF_DB_M = 0.034 # Might not be needed if not raw processing

# --- Pre-processed Acoustic Anchovy Data Parameters ---
# Parameters related to how the *external* detection was performed or how you interpret it.
# These might be thresholds used in Echoview outputs, or parameters for your own filtering of that output.
ANCHOVY_MIN_DEPTH_M = 0  # Minimum depth (m) for detected anchovy presence
ANCHOVY_MAX_DEPTH_M = 33.3  # Maximum depth (m) for detected anchovy presence
# Parameters below are for acoustic target characteristics from pre-processed data
# If you are filtering or re-visualizing based on these, keep them. Otherwise, you might remove.
PREPROCESSED_MIN_SV_DB = -91.0  # Example: Min acoustic volume backscatter (Sv) from Echoview
PREPROCESSED_MAX_SV_DB = -26.0  # Example: Max acoustic volume backscatter (Sv) from Echoview

# --- Environmental Data Parameters ---
# Parameters for integrating satellite and modelled data
SST_CHLA_SATELLITE_SOURCE = 'Copernicus'  # Example: 'Copernicus', 'MODIS'
SST_CHLA_RESOLUTION_KM = 1.0  # Example: 1 km resolution
OCEAN_CURRENT_MODEL_SOURCE = 'MyOcean'  # Example: 'MyOcean', 'HYCOM'

# --- Plotting & Visualization Parameters ---
DEFAULT_PLOT_DPI = 300  # Dots per inch for saved plots
PLOT_FORMAT = 'png'  # Default image format: 'png', 'svg', 'pdf'
COLORMAP_ACOUSTIC_DATA = 'viridis'  # Colormap for visualizing acoustic data (even if pre-processed)
COLORMAP_TEMPERATURE = 'thermal'  # Colormap for temperature plots
PLOT_TITLE_FONTSIZE = 14
PLOT_LABEL_FONTSIZE = 12

# --- Other General Project Constants ---
MISSING_DATA_VALUE = -999.0  # Standard value for missing data in processed outputs
SPEED_OF_SOUND_MPS = 1500.0  # Average speed of sound in seawater (adjust if needed for calculations)
