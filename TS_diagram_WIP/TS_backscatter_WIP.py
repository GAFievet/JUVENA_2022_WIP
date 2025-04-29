import gsw
import matplotlib.pyplot as plt
import numpy as np
from pot_dens_grid import generate_potential_density_grid

def TS_backscatter(ax, time, pressure, latitude, salinity, ptemp,backscatter):
	"""
	Takes all the following water sampling data along with a set of axis and returns a TS-depth diagram (scatter plot)
	over the given period of time.

	:param ax: Set of axes to scatter TS-backscatter on
	:param pressure: list of pressures
	:param latitude: list of latitudes
	:param time: list of datetime associates to each sampling
	:param salinity: list of salinity values
	:param ptemp: list of potential temperature
	:param backscatter: list backscattering values
	:param deepest_anchovy: Depth of the deepest anchovy found
	:return: scatter plot with salinity (x-axis), temperature (y-axis), density (diagonal), depth of sampling (
	colorscale)
	"""

	dep = -gsw.z_from_p(pressure, latitude)  # converting pressure to depth
	# Copy variable before change their size
	s, theta, dep = salinity.copy(), ptemp.copy(), dep.copy()
	# Flatten the data for the scatter
	dep, theta, s = dep.flatten(), theta.flatten(), s.flatten()

	# Generating background potential density contours & salinity, ptemp 2D arrays:
	si, thetai, dens = generate_potential_density_grid(s, theta)

	# Plotting background density contours:
	CS = ax.contour(si, thetai, dens, levels = np.arange(np.round(np.min(dens)), np.round(np.max(dens)) + 1, 0.5),
	                colors = 'k')
	ax.clabel(CS, inline = True, fontsize = 8)  # format labels
	ax.set_xlabel('Salinity (psu)', fontweight = 'bold', fontsize = 12)
	ax.set_ylabel('Theta (°C)', fontweight = 'bold', fontsize = 12)
	# plotting scatter plot of theta and s:
	# idx_depth = np.where(dep > -deepest_anchovy)[0]  # find idx of anchovy above deepest to plot only the data of
	# # interest WE ACTUTALLY WANT TO PLOT ALL CTD DATA
	# scatter = ax.scatter(s[idx_depth], theta[idx_depth], c = -dep[idx_depth], s = 4,cmap = 'jet')
	scatter = ax.scatter(s, theta, c = -dep, s = 4, cmap = 'jet')
	plt.colorbar(scatter, ax = ax, label = 'Depth (m)', orientation = 'vertical', extend = 'both').ax.invert_yaxis()
	# set a title
	ax.set_title(
		f"TS-depth diagram between {time(0).strftime("%d/%m/%Y HH:MM:SS")} and "
		f"{time(-1).strftime("%d/%m/%Y HH:MM:SS")}")

	return scatter
