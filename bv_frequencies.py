import os
from datetime import datetime, timedelta

import gsw  # Use gsw instead of seawater
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
# from matplotlib.text import Text
from matplotlib.ticker import MultipleLocator
# from mpl_toolkits.axes_grid1 import make_axes_locatable

# Load data from .mat file
p = os.path.join(r'C:\Users\G to the A\Desktop\MT\Programming\CTD',
                 'PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat')
data = sio.loadmat(p, squeeze_me = True)  # Squeeze arrays to avoid singletons
# Init. clear variables
date = data['time'][0:915]
cond = data['conductivity'][0:915]
depth = data['depth']
lon = data['longitude'][0:915]
lat = data['latitude'][0:915]
pressure = data['pressure'][0:915]
salinity = data['salinity'][0:915]
temp = data['temperature'][0:915]
# Convert to python-readable datetime
date = [(datetime(1, 1, 1) + timedelta(days = matlab_date - 367)) for matlab_date in date]
del data, p

# COMPUTE buoyancy frequency (N^2)
n2, p = gsw.Nsquared(salinity.T, temp.T, pressure.T, lat.T)
n = np.sqrt(np.abs(n2.T))  # Transpose n2 back and calculate N
n[np.isinf(n)] = np.nan
# n[n < 0.025] = np.nan
# FORMAT DATA FOR PLOTTING
x1 = date
y1 = depth[0:-1]
Z1 = n.T.tolist()
X1, Y1 = np.meshgrid(x1, y1)

# CREATE FIG
fig, axes = plt.subplots(3, 1, figsize = (11, 5))
# Adjust inter-plot padding
plt.subplots_adjust(hspace=1)

# CONTOUR
contourf = axes[0].contourf(X1, Y1, Z1, 30, cmap = 'jet')
# COLORBAR
# divider = make_axes_locatable(axes[0])
# cax = divider.append_axes("bottom", size="5%", pad=0.5)  # Adjust size and pad
# cax.set_visible(False)
cbar = fig.colorbar(contourf, ax = axes[0], orientation = 'horizontal')
cbar.set_label('BV freq. (rad/s)')

# Set depth limit to show
ylim = -210

###################### AVERAGING EVERY K METERS ######################
k = 5
depth_avg = [[] for i in range(210 // k)]
bv_mean = []
for i in range(1, 210, k):
	n_slice = n[:, i:i + k]  # Create (temporal) slices to average
	n_slice[np.all(np.isnan(n_slice), axis = 1)] = -999  # Attribute an outlier value to elements in full NaN rows
	bv_mean.append(np.nanmean(n_slice, axis = 1))  # Compute rows mean
	depth_avg[i // k] = np.nanmean(depth[i:i + k])  # Compute depth mean

bv_mean = np.array(bv_mean)
bv_mean[bv_mean == -999] = np.nan  # Get the outlier mean back to nan

# FORMAT DATA FOR PLOTTING
x2 = date
y2 = depth_avg
Z2 = bv_mean
X2, Y2 = np.meshgrid(x2, y2)

# CONTOUR
contourf = axes[1].contourf(X2, Y2, Z2, 30, cmap = 'jet')
# COLORBAR
cbar = fig.colorbar(contourf, ax = axes[1], orientation = 'horizontal')

###################### Plotting the sum of BV in the top 70m PLOTTING THE SUM(BV) IN THE TOP 70M ######################

sBV = np.nansum(n[:, 0:70], axis = 1)
axes[2].plot(date, sBV, '-b', lw = 1)


# FINE TUNE AXES
# Indicate the storm with a red frame
storm_start = mdates.date2num(datetime(2022, 9, 26))
storm_end = mdates.date2num(datetime(2022, 9, 30))
l = storm_end - storm_start

locator = mdates.AutoDateLocator()  # Automatically find tick positions
ylim=-210
date_num = mdates.date2num(date)
for ax in axes:
	# To create custom evenly spaced xticks
	# axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b-%d %H:%M'))
	# axes[0].set_xticks(np.linspace(date_num.min(), date_num.max(), 9))
	ax.xaxis.set_major_locator(locator)
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
	ax.set_ylabel('Depth (m)')
	ax.set_xlabel('Time')
	ax.set_xlim([date_num.min(), date_num.max()])

	# text = Text(storm_start + l / 2, ylim + 10 * 100 / abs(ylim), 'Storm', ha = 'center', va = 'center',
	# color = 'red',
	# fontsize = 11, )
	# ax.add_artist(text)  # Text
	rect = plt.Rectangle((storm_start, ylim), l, abs(ylim), facecolor = 'none', edgecolor = 'red', lw = 2)
	ax.add_patch(rect)  # Red frame
	if ax==axes[2]:
		ax.set_ylim([0.6, 1.1])
		ax.set_box_aspect(0.16)
		ax.yaxis.set_major_locator(MultipleLocator(0.1))
		# Show grid
		ax.grid(visible = True, which = 'both', axis = 'y')
	else:
		# Set ylim
		ax.set_ylim([ylim, 0])
		# Set box aspect
		ax.set_box_aspect(0.1)

ymin, ymax = axes[2].get_ylim()
rect = plt.Rectangle((storm_start, ymin), l, abs(ymax - ymin), facecolor = 'none', edgecolor = 'red', lw = 2)
axes[2].add_patch(rect)  # Red frame

# Layout
# plt.tight_layout(rect=[0, 0, 1, 0.95])
# Save fig
plt.savefig(r'C:\Users\G to the A\PycharmProjects\Paper\plots\BV_frequencies.png', transparent = False,
            bbox_inches = 'tight')

# Plot full size
# plt.show()
