import gsw
import numpy as np


def generate_potential_density_grid(abs_sal, cons_temp):
	"""
	Generates a potential density grid from abs_sal and potential temperature data.

	:param abs_sal: Array of absolute abs_sal values.
	:param cons_temp: Array of conservative temperature (= TEOS-10 while EOS-80 recommended potential temperature)
	:return: si (abs_sal array for contours), thetai (conservative temperature array for contours),dens (potential
	density array).
	"""

	# abs_sal range to compute potential density
	smin = np.nanmin(abs_sal) - 0.01 * np.nanmin(abs_sal)
	smax = np.nanmax(abs_sal) + 0.01 * np.nanmax(abs_sal)
	# temperature range to compute potential density
	thetamin = np.nanmin(cons_temp) - 0.1 * np.nanmax(cons_temp)
	thetamax = np.nanmax(cons_temp) + 0.1 * np.nanmax(cons_temp)
	# pot. density matrix resolution
	xdim = int(np.round((smax - smin) / 0.1 + 1))
	ydim = int(np.round((thetamax - thetamin) + 1))
	# init. potential density matrix
	pdens = np.zeros((ydim, xdim))
	# temperature & abs_sal matrix for pot. density computing
	thetai = np.arange(ydim) * 1 + thetamin
	si = np.arange(xdim) * 0.1 + smin
	# computing pot. density
	for j in range(ydim):
		for i in range(xdim):
			pdens[j,i] = gsw.rho(si[i], gsw.CT_from_pt(si[i], thetai[j]), 0) - 1000

	return si, thetai, pdens
