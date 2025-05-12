import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

from datetime_formating import matlab2python


def remap_acoustic_data(
		acoustic_data: pd.DataFrame,
		target_time: np.ndarray,
		target_depth: np.ndarray,
		time_col: str = "Time",
		depth_col: str = "Depth_start",
		acoustic_signal_col: str = "Sv",
) -> np.ndarray:
	"""
	    Remaps acoustic backscatter data onto the time/depth grid of a target dataset
	    (e.g., temperature/salinity) for comparison.

	    Args:
	        acoustic_data (pd.DataFrame): DataFrame containing acoustic data with
	                                     time, depth, and acoustic signal columns.
	                                     Time is expected to be in MATLAB datenum format.
	        target_time (np.ndarray): 1D array of time values from the target dataset
	                                 (in datetime objects).
	        target_depth (np.ndarray): 1D array of depth values from the target dataset.
	        time_col (str, optional): Name of the time column in acoustic_data.
	                                 Defaults to "Time".
	        depth_col (str, optional): Name of the depth column in acoustic_data.
	                                 Defaults to "Depth_start".
	        acoustic_signal_col (str, optional): Name of the acoustic signal column
	                                            in acoustic_data. Defaults to "Sv".

	    Returns:
	        np.ndarray: 1D array of remapped acoustic backscatter values,
	                  interpolated onto the target time/depth grid. NaN values
	                  indicate locations where the target grid has points but
	                  the acoustic data does not have corresponding measurements.

	    Raises:
	        ValueError: If acoustic_data is empty.
	    """

	if acoustic_data.empty:
		raise ValueError("Acoustic data DataFrame cannot be empty.")

	# 1. Extract acoustic data and convert time to Python datetime
	acoustic_time_matlab = acoustic_data[time_col].values
	acoustic_depth = acoustic_data[depth_col].values
	acoustic_signal = acoustic_data[acoustic_signal_col].values
	acoustic_time = np.array([matlab2python(t) for t in acoustic_time_matlab])

	# 2. Create a mapping function (interpolator)
	#    - Use acoustic time/depth pairs as the grid for the interpolator
	acoustic_time_unique = np.unique(acoustic_time)
	acoustic_depth_unique = np.unique(acoustic_depth)

	#    - Create a mapping from (time, depth) to acoustic signal (linear scale)
	#      We need to find the indices of each acoustic measurement in the unique arrays
	time_indices = np.searchsorted(acoustic_time_unique, acoustic_time) - 1
	depth_indices = np.searchsorted(acoustic_depth_unique, acoustic_depth) - 1

	#    - Construct the acoustic signal matrix
	acoustic_signal_matrix = np.zeros((len(acoustic_time_unique), len(acoustic_depth_unique)))

	#    - Populate the matrix with the linear acoustic signal values
	#      Handle potential out-of-bounds indices from searchsorted
	valid_time_indices = (time_indices >= 0) & (time_indices < len(acoustic_time_unique))
	#      Create a boolean mask indicating which time indices are within the valid range
	valid_depth_indices = (depth_indices >= 0) & (depth_indices < len(acoustic_depth_unique))
	#      Create a boolean mask indicating which depth indices are within the valid range
	valid_measurements = valid_time_indices & valid_depth_indices
	#      Combine the time and depth validity checks.
	#      Only use data points where both time and depth indices are valid (within the bounds of unique values)

	acoustic_signal_matrix[time_indices[valid_measurements], depth_indices[valid_measurements]] = 10 ** (
			acoustic_signal[valid_measurements] / 10)

	interpolator = RegularGridInterpolator(
		(acoustic_time_unique, -acoustic_depth_unique),  # Invert depth for consistency
		acoustic_signal_matrix.T,
		method = "linear",  # Or consider "nearest"
		bounds_error = False,
		fill_value = np.nan,
	)

	# 3. Generate target grid coordinates
	target_time_grid, target_depth_grid = np.meshgrid(target_time, -target_depth)  # Invert depth
	target_points = np.stack((target_time_grid, target_depth_grid), axis = -1)

	# 4. Remap acoustic data onto the target grid
	remapped_acoustic_signal = interpolator(target_points).flatten()

	# 5. Convert back to dB
	remapped_acoustic_signal[remapped_acoustic_signal != 0] = 10 * np.log10(
		remapped_acoustic_signal[remapped_acoustic_signal != 0]
	)
	remapped_acoustic_signal[remapped_acoustic_signal == 0] = np.nan  # Ensure 0s become NaN

	return remapped_acoustic_signal