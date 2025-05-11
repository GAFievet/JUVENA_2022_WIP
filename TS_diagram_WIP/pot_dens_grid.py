import gsw
import numpy as np


def generate_potential_density_grid(salinity, ptemp):
	"""
	Generates a potential density grid from salinity and potential temperature data.

	:param salinity: Array of salinity values.
	:param ptemp: Array of potential temperature values.
	:return: si (salinity array for contours), thetai (potential temperature array for contours),dens (potential
	density array).
	"""

	# salinity range to compute potential density
	smin = np.nanmin(salinity) - 0.01 * np.nanmin(salinity)
	smax = np.nanmax(salinity) + 0.01 * np.nanmax(salinity)
	# temperature range to compute potential density
	thetamin = np.nanmin(ptemp) - 0.1 * np.nanmax(ptemp)
	thetamax = np.nanmax(ptemp) + 0.1 * np.nanmax(ptemp)
	# pot. density matrix resolution
	xdim = int(np.round((smax - smin) / 0.1 + 1))
	ydim = int(np.round((thetamax - thetamin) + 1))
	# init. potential density matrix
	dens = np.zeros((ydim, xdim))
	# temperature & salinity matrix for pot. density computing
	thetai = np.arange(ydim) * 1 + thetamin
	si = np.arange(xdim) * 0.1 + smin
	# computing pot. density
	for j in range(ydim):
		for i in range(xdim):
			dens[j, i] = gsw.dens(si[i], thetai[j], 0)
	dens = dens - 1000  # Typical notation with 1000 kg/m3 removed

	return si, thetai, dens
