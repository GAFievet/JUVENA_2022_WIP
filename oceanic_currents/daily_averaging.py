import datetime
import pickle
import numpy as np
from datetime_formating import matlab2python
"""
Used to average surface oceanic current's velocity components for each calendar day after being low-passed.
"""


def calculate_daily_average_component(u, t):
	"""
	Calculates the daily average of an oceanic current's component.

	Args:
		u (numpy.ndarray): A 3D NumPy array representing the velocity of the
			oceanic current along the u-component.
			Dimensions: (longitude, latitude, time).
		t (numpy.ndarray): A 1D NumPy array containing datetime objects
			corresponding to the time dimension of the 'u' array.

	Returns:
		numpy.ndarray: A 3D NumPy array with the same longitude and latitude
			dimensions as 'u', but the time dimension is replaced with daily
			averages.  The time dimension will have a length equal to the number of unique days.
			For example, if u is (5, 10, 365) then the output will be (5, 10, N)
			where N is the number of unique days in the original 365 days.
			Values in the output array represent the average u-component velocity
			for each day at each longitude and latitude.
			If a day has no measurements, the corresponding slice in the
			output array will contain NaNs.
	"""
	# 1. Get the unique days from the datetime array `t`.
	t=np.squeeze(t) # Make sure its squeezed
	t= [matlab2python(date) for date in t]
	unique_days = np.unique([date.toordinal() for date in t])  # Use ordinal representation for efficient comparison
	num_days = len(unique_days)

	# 2. Create an empty array to store the daily averages.  Initialize with NaN.
	u_daily_averaged = np.full((u.shape[0], u.shape[1], num_days), np.nan, dtype = u.dtype)

	# 3. Iterate through each unique day.
	t2 = []  # Initialize an empty list to store the unique days as datetime objects
	for i, day_ordinal in enumerate(unique_days):
		# Convert the ordinal back to a datetime object for comparison.
		day_dt = datetime.datetime.fromordinal(day_ordinal)
		t2.append(day_dt.date())  # Append the datetime object to the t2 list

		# Create a boolean mask to find the time indices corresponding to the current day.
		daily_mask = np.array([(date.toordinal() == day_ordinal) for date in t])

		# 4. Calculate the daily average for each longitude and latitude.
		if np.any(daily_mask):  # Check if there are any measurements for the current day.
			u_daily_averaged[:, :, i] = np.nanmean(u[:, :, daily_mask], axis = 2)

	return u_daily_averaged, t2


def calculate_average_current(u, v, t):
	"""
	Calculates daily averages for both component of the oceanic current
	Assuming there will be no days for which one component is known and the other is not.
	"""
	u_daily_averaged, t2 = calculate_daily_average_component(u, t)
	v_daily_averaged, t2 = calculate_daily_average_component(v, t)
	return u_daily_averaged, v_daily_averaged, t2


if __name__ == '__main__':

	path2file = r'../data/surface_currents/IBI_data_filt.pkl'
	try:
		with open(path2file, 'rb') as f:
			data_flt = pickle.load(f)
			print(f"The file '{path2file}' was imported successfully.")
		u_flt, v_flt, t = data_flt['u_flt'], data_flt['v_flt'], data_flt['time_ibi']
		# Data of interest (23/09/2022 and on) starts after
		u_flt=u_flt[:,:,73:]
		v_flt=v_flt[:,:,73:]
		t=np.squeeze(t)
		t=t[73:]

		# Average signals for each calendar days
		u_d_avg, v_d_avg, t2 = calculate_average_current(u_flt, v_flt, t)

		# Create new file to save adding the newly created variables
		IBI_data_filt_avg = data_flt.copy()
		IBI_data_filt_avg['u_d_avg'] = u_d_avg
		IBI_data_filt_avg['v_d_avg'] = v_d_avg
		IBI_data_filt_avg['t2'] = t2

		# Save the new data along the old one in a pickle file
		with open(r'../data/surface_currents/IBI_data_filt_avg.pkl', 'wb') as f:
			pickle.dump(IBI_data_filt_avg, f)
			print(f"The variable was saved successfully.")
	except FileNotFoundError:
		print(f"Error: The file '{path2file}' was not found.")
	except Exception as e:
		print(f"An error occurred while importing the file: {e}")
