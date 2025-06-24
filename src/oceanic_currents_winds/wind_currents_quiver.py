from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import config


def load_and_clean_data(file_path: str) -> pd.DataFrame:
	"""
	Loads raw data from a CSV file, cleans it, and performs initial preprocessing.

	Args:
		file_path (str): The path to the raw data CSV file.

	Returns:
		pd.DataFrame: The cleaned and preprocessed DataFrame.
	"""
	# print(f"Loading and cleaning data from: {file_path}")
	# Load the dataset, skipping the first row and using the second row as header
	df = pd.read_csv(file_path, sep = '\t', header = 1)

	# Rename columns for better readability
	df.rename(columns = {
		'Fecha (GMT)': 'Timestamp',
		'Velocidad media de Corriente(cm/s)': 'current_speed_cm_s',
		'Dir. de prop. de la Corriente(0=N,90=E)': 'current_direction',
		'Velocidad media del viento(m/s)': 'wind_speed_m_s',
		'Direc. de proced. del Viento(0=N,90=E)': 'wind_direction'
	}, inplace = True)

	# Select only columns of interest
	df = df[['Timestamp', 'current_speed_cm_s', 'current_direction', 'wind_speed_m_s', 'wind_direction']]

	# Replace non-numeric placeholders with NaN and convert to numeric.
	# errors='coerce' will turn any non-convertible values into NaN.
	for col in ['current_speed_cm_s', 'current_direction', 'wind_speed_m_s', 'wind_direction']:
		df[col] = pd.to_numeric(df[col], errors = 'coerce')
		# Replace the specific value -9999.9 by NaN
		df[col] = df[col].replace(-9999.9, np.nan)

	# Convert cm/s to m/s for current speed
	df['current_speed_m_s'] = df['current_speed_cm_s'] / 100.0

	# Drop rows with missing values in the relevant columns
	initial_rows = len(df)
	df.dropna(subset = ['current_speed_m_s', 'current_direction', 'wind_speed_m_s', 'wind_direction', 'Timestamp'],
	          inplace = True)
	# print(f"Dropped {initial_rows - len(df)} rows with missing values.")

	# Convert 'Timestamp' to datetime objects
	df['Timestamp'] = pd.to_datetime(df['Timestamp'], format = '%Y %m %d %H')

	# print("Data cleaning complete.")
	pd.set_option('display.max_columns', None)
	# print(df.describe(include = 'all'))
	return df


def calculate_vector_components(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Calculates the U and V components for wind and current.

	Args:
		df (pd.DataFrame): The DataFrame containing speed and direction data.

	Returns:
		pd.DataFrame: The DataFrame with the new U and V component columns.
	"""
	# print("Calculating vector components for wind and current...")
	# For wind direction (coming from), meteorological convention
	df['wind_direction_rad'] = np.deg2rad(df['wind_direction'])
	# The u (east-west) and v (north-south) components are calculated.
	# For meteorological convention, u is eastward speed and v is northward speed.
	# However, if the direction is "from where the wind comes", we need to invert the signs
	# to get the direction it goes (which is what quivers typically represent).
	df['wind_u'] = -df['wind_speed_m_s'] * np.sin(df['wind_direction_rad'])
	df['wind_v'] = -df['wind_speed_m_s'] * np.cos(df['wind_direction_rad'])

	# For current direction (going to), oceanographic convention
	df['current_direction_rad'] = np.deg2rad(df['current_direction'])
	# For current, the direction is where it's moving towards.
	df['current_u'] = df['current_speed_m_s'] * np.sin(df['current_direction_rad'])
	df['current_v'] = df['current_speed_m_s'] * np.cos(df['current_direction_rad'])

	# print("Component calculation complete.")
	return df


def plot_quiver_data(df: pd.DataFrame, save_path: str, dpi: int):
	"""
	Plots wind and current vectors using quiver plots.

	Args:
		df (pd.DataFrame): The DataFrame containing the U and V components, as well as timestamps.
		save_path (str): The path to save the figure.
		dpi (int): The resolution (dots per inch) of the saved figure.
	"""
	# print(f"Creating quiver plot and saving to: {save_path}")
	# Create the figure and subplots
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (15, 12))
	# Plot wind vectors in the top subplot
	# Q1 is the Quiver object to allow adding a scale key
	Q1 = ax1.quiver(df['Timestamp'], np.zeros(len(df)), df['wind_u'], df['wind_v'],
	                color = 'k', scale = 5, width = 0.002, scale_units = "inches", headlength = 1, headwidth = 1,
	                headaxislength
	                = 1)

	ax1.set_ylabel('')  # Remove y-label
	ax1.set_yticks([])  # Remove y-ticks
	ax1.set_title('Winds')  # Add a title for clarity
	ax1.grid(True, linestyle = '--', alpha = 0.7)  # Add a grid for better readability

	# Add a scale key for wind
	ax1.quiverkey(Q1, X = 0.95, Y = 0.85, U = 2, label = '2 m/s Wind', labelpos = 'W', coordinates = 'axes',
	              fontproperties = fm.FontProperties(size = 12))

	##### CURRENTS #####
	# Plot current vectors in the bottom subplot
	Q2 = ax2.quiver(df['Timestamp'], np.zeros(len(df)), df['current_u'], df['current_v'],
	                color = 'k', scale = 0.3, width = 0.002, scale_units = "inches", headlength = 1, headwidth = 1,
	                headaxislength = 1)

	ax2.set_ylabel('')  # Remove y-label
	ax2.set_yticks([])  # Remove y-ticks
	ax2.set_title('Surface currents')  # Add a title for clarity
	ax2.grid(True, linestyle = '--', alpha = 0.7)  # Add a grid

	# Add a scale key for current
	ax2.quiverkey(Q2, X = 0.95, Y = 0.85, U = 0.1, label = '0.1 m/s Current', labelpos = 'W', coordinates = 'axes',
	              fontproperties = fm.FontProperties(size = 12))

	# Add gale indication
	gale_start = datetime.strptime("26/09/2022 00:00:00", "%d/%m/%Y %H:%M:%S")
	gale_end = datetime.strptime("30/09/2022 23:59:59", "%d/%m/%Y %H:%M:%S")
	l = gale_end - gale_start
	# ax1 lim
	ymin, ymax = ax1.get_ylim()
	rect = plt.Rectangle((gale_start, ymin), l, abs(ymax - ymin), facecolor = 'blue', alpha = 0.1, label = "Gale")
	ax1.add_patch(rect)
	# ax2 lim
	ymin, ymax = ax2.get_ylim()
	rect = plt.Rectangle((gale_start, ymin), l, abs(ymax - ymin), facecolor = 'blue', alpha = 0.1, label = "Gale")
	ax2.add_patch(rect)

	# Format the x-axis for dates
	date_form = mdates.DateFormatter('%b-%d')
	ax1.xaxis.set_major_formatter(date_form)
	plt.xticks(ha = 'right', fontsize = 12)  # Rotate x-axis labels to prevent overlap
	ax2.sharex(ax1)

	# Legend
	ax1.legend(loc = 'upper right', framealpha = 1, facecolor = "white", edgecolor = 'black', fancybox = True)
	ax2.legend(loc = 'upper right', framealpha = 1, facecolor = "white", edgecolor = 'black', fancybox = True)

	plt.setp(ax2.get_xticklabels(), visible = False)
	# Save the figure
	plt.savefig(save_path, transparent = False, dpi = dpi, bbox_inches = "tight")


# plt.show() # Display the figure after saving


def main():
	"""
	Main function to execute the data analysis workflow.
	"""
	# print("Starting wind and current data analysis.")

	# 1. Load and clean the data using the path from config
	df = load_and_clean_data(config.RAW_BUOY_DATA)

	# 2. Calculate vector components
	df = calculate_vector_components(df)

	# 3. Plot the data and save the figure using paths and DPI from config
	plot_quiver_data(df, config.BUOY_QUIVER, config.DEFAULT_PLOT_DPI)


# print("Wind and current data analysis completed.")


if __name__ == "__main__":
	main()
