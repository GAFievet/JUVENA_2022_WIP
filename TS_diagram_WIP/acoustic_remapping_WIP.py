import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from scipy.sparse import csr_matrix

from datetime_formating import matlab2python


def remap_acoustic_data(
		acoustic_data: pd.DataFrame,
		target_time: np.ndarray,
		target_depth: np.ndarray,
		time_col: str = "Time",
		depth_col: str = "Depth_start",
		acoustic_signal_col: str = "Sv",
		interpolation_method: str = "linear",
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
		interpolation_method (str, optional): Interpolation method to use.
											 Defaults to "linear".

	Returns:
		np.ndarray: 1D array of remapped acoustic backscatter values,
				  interpolated onto the target time/depth grid. NaN values
				  indicate locations where the target grid has points but
				  the acoustic data does not have corresponding measurements.

	Raises:
		ValueError: If input data is invalid or empty, or if interpolation
					method is not supported.
		TypeError: If input arguments have incorrect types.
		KeyError: If specified columns are not found in acoustic_data.
	"""
	# 0. Parameter Validation
	if not isinstance(acoustic_data, pd.DataFrame):
		raise TypeError("acoustic_data must be a Pandas DataFrame.")
	if acoustic_data.empty:
		raise ValueError("acoustic_data cannot be empty.")
	if not isinstance(target_time, np.ndarray):
		raise TypeError("target_time must be a NumPy array.")
	if not isinstance(target_depth, np.ndarray):
		raise TypeError("target_depth must be a NumPy array.")
	if target_time.ndim != 1:
		raise ValueError("target_time must be a 1D array.")
	if target_depth.ndim != 1:
		raise ValueError("target_depth must be a 1D array.")
	if not isinstance(time_col, str):
		raise TypeError("time_col must be a string.")
	if not isinstance(depth_col, str):
		raise TypeError("depth_col must be a string.")
	if not isinstance(acoustic_signal_col, str):
		raise TypeError("acoustic_signal_col must be a string.")
	if not isinstance(interpolation_method, str):
		raise TypeError("interpolation_method must be a string.")
	if interpolation_method not in ["linear", "nearest"]:
		raise ValueError(
			f"Invalid interpolation_method: '{interpolation_method}'. Supported methods are 'linear' and 'nearest'."
		)
	if time_col not in acoustic_data.columns:
		raise KeyError(f"Column '{time_col}' not found in acoustic_data.")
	if depth_col not in acoustic_data.columns:
		raise KeyError(f"Column '{depth_col}' not found in acoustic_data.")
	if acoustic_signal_col not in acoustic_data.columns:
		raise KeyError(f"Column '{acoustic_signal_col}' not found in acoustic_data.")

	try:
		# 1. Extract acoustic data and convert time to Python datetime
		acoustic_time_matlab = acoustic_data[time_col].values
		acoustic_depth = acoustic_data[depth_col].values
		acoustic_signal = acoustic_data[acoustic_signal_col].values
		acoustic_time = np.array([matlab2python(t) for t in acoustic_time_matlab])

		# 2. Create a mapping function (interpolator)
		acoustic_time_unique = np.unique(acoustic_time)
		acoustic_depth_unique = np.unique(acoustic_depth)

		time_indices = np.searchsorted(acoustic_time_unique, acoustic_time) - 1
		depth_indices = np.searchsorted(acoustic_depth_unique, acoustic_depth) - 1

		# --- Sparse Matrix Creation ---
		valid_time_indices = (time_indices >= 0) & (time_indices < len(acoustic_time_unique))
		valid_depth_indices = (depth_indices >= 0) & (depth_indices < len(acoustic_depth_unique))
		valid_measurements = valid_time_indices & valid_depth_indices

		sparse_data = 10 ** (acoustic_signal[valid_measurements] / 10)  # Convert Sv to linear scale
		sparse_row_indices = time_indices[valid_measurements]
		sparse_col_indices = depth_indices[valid_measurements]

		acoustic_signal_matrix = csr_matrix(
			(sparse_data, (sparse_row_indices, sparse_col_indices)),
			shape = (len(acoustic_time_unique), len(acoustic_depth_unique)),
		)
		# --- End Sparse Matrix Creation ---

		# Invert depth for consistency with oceanographic convention (depth increases downwards)
		interpolator = RegularGridInterpolator(
			([d.timestamp() for d in acoustic_time_unique], -acoustic_depth_unique),
			acoustic_signal_matrix,
			method = interpolation_method,
			bounds_error = False,
			fill_value = np.nan,  # Use NaN for points outside the input data's convex hull
		)

		# 3. Generate target grid coordinates
		# Invert depth for consistency with oceanographic convention
		target_time_grid, target_depth_grid = np.meshgrid(target_time, -target_depth)
		target_points = np.stack((target_time_grid, target_depth_grid), axis = -1)

		# 4. Remap acoustic data onto the target grid
		remapped_acoustic_signal = interpolator(target_points).flatten()

		# 5. Convert back to dB
		remapped_acoustic_signal[remapped_acoustic_signal != 0] = 10 * np.log10(
			remapped_acoustic_signal[remapped_acoustic_signal != 0]
		)
		remapped_acoustic_signal[remapped_acoustic_signal == 0] = np.nan  # Ensure 0s become NaN

		return remapped_acoustic_signal

	except Exception as e:
		raise Exception(f"An unexpected error occurred during the remapping process: {e}")
