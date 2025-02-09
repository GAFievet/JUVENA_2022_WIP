import os
from datetime import datetime, timedelta

import gsw  # Use gsw instead of seawater
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

# Load data
p = os.path.join(r'C:\Users\G to the A\Desktop\MT\Programming\CTD',
                 'PROCESSED_data_POS_CORRECTED_above2mREMOVED_ww11.mat')
data = sio.loadmat(p)
data['time'] = data['time'][0:915]
# Convert from ndarray
data['time'] = [float(x.item()) for x in data['time']]
# Convert from numerical to datetime list with python epoch
data['time'] = [(datetime(1, 1, 1) + timedelta(days = matlab_date - 367)) for matlab_date in data['time']]

date = data['time']

# Calculate buoyancy frequency (N^2)
n2 = gsw.Nsquared(data['salinity'].T, data['temperature'].T, data['pressure'].T, data['latitude'].T)[0]
n = np.sqrt(np.abs(n2.T))  # Transpose n2 back and calculate N
n[np.isinf(n)] = np.nan
n = n[0:915, :]
# n[n < 0.025] = np.nan

# Plotting the Hovmoller diagram
fig, ax = plt.subplots(figsize = (10, 2.5))
x = data['time']
y = data['depth'][0:-1]
Z = n.T.tolist()
X, Y = np.meshgrid(x, y)

contourf = ax.contourf(X, Y, Z, 30, cmap = 'jet')

date_num = mdates.date2num(data['time'])

# To create custom evenly spaced xticks
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d %H:%M'))
# ax.set_xticks(np.linspace(date_num.min(), date_num.max(), 9))

locator = mdates.AutoDateLocator()  # Automatically find tick positions
formatter = mdates.AutoDateFormatter(locator)  # Automatically format dates
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

# To format the ticks
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))

ax.set_ylabel('Depth (m)')
ax.set_xlabel('Time')
cbar = fig.colorbar(contourf, ax = ax, orientation = 'horizontal')

cbar.set_label('BV freq. (Hz)')
ylim=-100
ax.set_ylim([ylim, 0])
ax.set_xlim([date_num.min(), date_num.max()])

storm_start = mdates.date2num(datetime(2022, 9, 26))
storm_end = mdates.date2num(datetime(2022, 9, 30))
rect = plt.Rectangle((storm_start, ylim), storm_end - storm_start, abs(ylim), facecolor = 'red',
                     edgecolor = 'red', lw = 2)

plt.tight_layout()
plt.show()

# # Averaging every k meters
# k = 5
# z = []
# bv_mean = []
# for i in range(0, 210, k):
# 	bv_mean.append(np.nanmean(n[:, i:i + k], axis = 1))
# 	z.append(np.nanmean(data['depth'][i:i + k]))
#
# bv_mean = np.array(bv_mean).T
# z = np.array(z)
#
# # Plotting the averaged Hovmoller diagram
# fig, ax = plt.subplots(figsize = (8, 2.5))
# contourf = ax.contourf(data['time'], z, bv_mean, 300, cmap = 'jet')
# ax.set_xticks(np.arange(mdates.date2num(datetime.fromordinal(int(date[0]))),
#                         mdates.date2num(datetime.fromordinal(int(date[-2]))) + 1, (
# 		                        mdates.date2num(datetime.fromordinal(int(date[-2]))) - mdates.date2num(
# 	                        datetime.fromordinal(int(date[0])))) / 7))
# ax.set_xticklabels([datetime.fromordinal(int(d)).strftime('%b-%d %H:%M') for d in
#                     np.arange(date[0], date[-1], (date[-1] - date[0]) / 7)])
# ax.set_ylabel('Depth (m)')
# cbar = fig.colorbar(contourf)
# cbar.set_label('BV freq. (Hz)')
# ax.set_ylim([-210, 0])
# ax.set_xlim([date[0], date[-2]])
# ax.set_box_aspect(8 / 210)
# plt.tight_layout()
# plt.show()
#
# # Plotting the sum of BV in the top 70m
# sBV = np.nansum(n[:, 0:70], axis = 1)
#
# fig, ax = plt.subplots(figsize = (8, 2.5))
# ax.plot(data['time'], sBV)
# ax.set_xticks(np.arange(mdates.date2num(datetime.fromordinal(int(date[0]))),
#                         mdates.date2num(datetime.fromordinal(int(date[-2]))) + 1, (
# 		                        mdates.date2num(datetime.fromordinal(int(date[-2]))) - mdates.date2num(
# 	                        datetime.fromordinal(int(date[0])))) / 7))
# ax.set_xticklabels([datetime.fromordinal(int(d)).strftime('%b-%d %H:%M') for d in
#                     np.arange(date[0], date[-1], (date[-1] - date[0]) / 7)])
# ax.set_ylabel('Stratification')
# ax.set_ylim([0.6, 1.1])
# ax.set_xlim([date[0], date[-2]])
# ax.set_box_aspect(8 / 0.5)
# plt.tight_layout()
# plt.show()
