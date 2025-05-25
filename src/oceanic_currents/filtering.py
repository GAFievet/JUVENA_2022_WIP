import pickle

import numpy as np
import scipy.io

from butfilt import butfilt

"""
Uses butfilt.py to apply a low pass filter to surface oceanic current's velocity components.
Next step is to average the returned data over a calendar day. See daily_averaging.py  
"""

def filter_data(data_u: np.ndarray, data_v: np.ndarray, filtering_freq=72) -> tuple[np.ndarray, np.ndarray]:
	"""
	Filters the input data_u and data_v using a Butterworth filter.

	Args:
		data_u (np.ndarray): 3D NumPy array containing u-component data (time series in the 3rd dimension).
		data_v (np.ndarray): 3D NumPy array containing v-component data (time series in the 3rd dimension).
		filtering_freq (float):  The cutoff frequency for the filter (in hours).

	Returns:
		tuple[np.ndarray, np.ndarray]: A tuple containing the filtered u-component data (serie_u_filt) and the
		filtered v-component data (serie_v_filt), both as a 3D NumPy array.
	"""

	serie_u_filt = np.zeros_like(data_u)  # Create a matrix of 0s like data_u
	serie_v_filt = np.zeros_like(data_v)  # Create a matrix of 0s like data_v

	for dd in range(data_u.shape[0]):  # Loop through the first dimension of data_u
		for aa in range(data_u.shape[1]):  # Loop through the second dimension of data_u
			# Extract time series and handle NaNs for u-component
			serie_u = data_u[dd, aa, :].copy()  # Extract time series
			loc_nan_u = np.isnan(serie_u)  # Find NaN locations
			serie_u[loc_nan_u] = 0  # Replace NaNs with 0s

			# Extract time series and handle NaNs for v-component
			serie_v = data_v[dd, aa, :].copy()  # Extract time series
			loc_nan_v = np.isnan(serie_v)
			serie_v[loc_nan_v] = 0

			# Filter the time series
			serie_u_filtdd = butfilt(filtering_freq, serie_u, 3600)  # hourly currents, hence, 3600s sampling rate
			serie_v_filtdd = butfilt(filtering_freq, serie_v, 3600)

			# Restore NaNs in the filtered data
			serie_u_filtdd[loc_nan_u] = np.nan
			serie_v_filtdd[loc_nan_v] = np.nan

			# Assign the filtered time series to the output arrays
			serie_u_filt[dd, aa, :] = serie_u_filtdd
			serie_v_filt[dd, aa, :] = serie_v_filtdd

	return serie_u_filt, serie_v_filt


if __name__ == '__main__':

	path2file = r'../data/surface_currents/IBI_data.mat'
	try:
		IBI_data = scipy.io.loadmat(path2file)
		print(f"The file '{path2file}' was imported successfully.")
		u_flt, v_flt = filter_data(IBI_data['u_ibi'], IBI_data['v_ibi'])
		IBI_data['u_flt'], IBI_data['v_flt'] = u_flt, v_flt
		# Save the new data along the old one in a pickle file
		with open(r'../../data/surface_currents/IBI_data_filt.pkl', 'wb') as f:
			pickle.dump(IBI_data, f)
			print(f"The variable was saved successfully.")
	except FileNotFoundError:
		print(f"Error: The file '{path2file}' was not found.")
	except Exception as e:
		print(f"An error occurred while importing the file: {e}")
