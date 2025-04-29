import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.text import Text

# Read daily glider GPS files
directory = r'data/glider/Daily_GPS'
all_files = os.listdir(directory)
csv_files = [f for f in all_files if f.endswith('.csv')]
days = []
for file in csv_files:
	df_gps = pd.read_csv(os.path.join(directory, file))
	day = datetime.strptime(df_gps["GPS_date"].iloc[len(df_gps["GPS_date"]) // 2], "%d-%b-%Y")
	if datetime(2022, 9, 23) <= day <= datetime(2022, 10, 6):
		days.append(day)
		min_lat = min(df_gps["Latitude"])
		max_lat = max(df_gps["Latitude"])

		plt.plot([day, day], [min_lat, max_lat], '-', c = "#F8766D", lw = 1.5)

# Read daily glider acoustic files
directory = r'data/glider'
all_files = os.listdir(directory)
csv_files = [f for f in all_files if f.endswith('.csv') and f != "Glider.gps.csv"]
for file in csv_files:
	df = pd.read_csv(os.path.join(directory, file))
	start_idx = None
	relay_idx = start_idx

	# Loop through df
	for i in range(len(df)):
		# Default values for conditions 1 and 2
		condition1 = False
		condition2 = False
		if relay_idx is not None:  # Sets conditions for plotting
			condition1 = abs(df['Latitude_avg'].iloc[i] - df['Latitude_avg'].iloc[relay_idx]) < 1
			condition2 = (datetime.strptime(df["Time_avg_UTC"].iloc[i], "%d/%m/%Y %H:%M:%S").date() ==
			              datetime.strptime(df["Time_avg_UTC"].iloc[relay_idx], "%d/%m/%Y %H:%M:%S").date())
		if df["Sv_lin"].iloc[i] != 0 and start_idx is None:  # Initiate a series of anchovy
			start_idx = i  # Mark the beginning of a non-zero sequence
			relay_idx = start_idx  # Mark the relay idx
		elif df["Sv_lin"].iloc[i] != 0 and start_idx is not None and condition1 and condition2:
			relay_idx = i  # Mark the relay idx of a non-zero sequence
		elif df["Sv_lin"].iloc[i] == 0 and start_idx is not None and not (condition1 and condition2):
			# Plot the line for the previous non-zero sequence
			day = datetime.strptime(df["Time_avg_UTC"].iloc[start_idx], "%d/%m/%Y %H:%M:%S").date()
			x = [day, day]
			y = [df["Latitude_avg"].iloc[start_idx], df["Latitude_avg"].iloc[relay_idx]]
			plt.plot(x, y, '-', c = "#F8766D", lw = 3)
			start_idx = None  # Reset for the next sequence

		if start_idx is not None:
			# Plot the line for the previous non-zero sequence
			day = datetime.strptime(df['Time_avg_UTC'].iloc[start_idx], "%d/%m/%Y %H:%M:%S").date()
			x = [day, day]
			y = [df["Latitude_avg"].iloc[start_idx], df["Latitude_avg"].iloc[- 1]]
			plt.plot(x, y, '-', c = "#F8766D", lw = 3)

# color vessel
# "#01BEC3"

# Format the x-axis (without the year)
plt.gca().xaxis.set_major_formatter(
	mdates.DateFormatter('%d/%m'))  # %b: Abbreviated month name, %d: Day of the month
# Format the x-axis to show dates nicely
plt.gcf().autofmt_xdate()  # Automatically formats the dates

plt.xlabel("Date")
plt.ylabel("Latitude")

plt.xticks(days)
plt.tight_layout()
plt.grid()

# Manually create a legend
# Anchovy (black filled rectangle)
anchovy_patch = Line2D([0], [0],color = 'black', linewidth = 3, label = 'Anchovy', visible = True)

# Coverage (black line)
coverage_line = Line2D([0], [0], color = 'black', linewidth = 1.5, label = 'Coverage', visible = True)

# Glider (red line)
glider_line = Line2D([0], [0], color = "#F8766D", linewidth = 1, label = 'Glider')

# Vessel (cyan line)
vessel_line = Line2D([0], [0], color = "#01BEC3", linewidth = 1, label = 'Vessel')

# Legend titles
type_pos_title = Text(0, 0, 'Data type', fontweight = 'bold')
platform_type_title = Text(0, 0, 'Platform type', fontweight = 'bold')

# Create dummy patches with invisible face colors to act as handles
type_pos_patch = Patch(facecolor = 'none', edgecolor = 'none', label = type_pos_title)
platform_type_patch = Patch(facecolor = 'none', edgecolor = 'none', label = platform_type_title)

# Create the legend with custom elements
legend = plt.legend(
	handles = [anchovy_patch, coverage_line, glider_line, vessel_line],
	loc = "lower right",  # Adjust location as needed
	frameon = True,  # Keeps frame around legend
	fontsize = 10)  # Adjust font size as needed

# plt.legend(loc = 'lower right')

# Save fig
plt.savefig(r'plots/anchovy_detection.png', transparent = True,
            bbox_inches = 'tight')

plt.show()
