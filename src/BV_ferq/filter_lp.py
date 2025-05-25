import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import filtfilt

from src.BV_ferq.bv_frequencies import load_dot_mat_CTD, compute_bv_freq, bv_freq_avg_every_k_meters


def get_sampling_freq_total_time(signal, time_days):
	num_samples = len(signal)
	# 1. Determine the sampling frequency
	total_time_seconds = time_days * 24 * 3600  # Total time in seconds
	sampling_frequency = num_samples / total_time_seconds  # Samples per second
	return sampling_frequency, total_time_seconds


def get_cutoff_freq_norm(cutoff_freq_h, total_time_seconds):
	# 2. Design the filter
	cutoff_frequency_hours = cutoff_freq_h  # Cutoff frequency in hours
	cutoff_frequency_seconds = cutoff_frequency_hours * 3600  # Cutoff freq in seconds
	cutoff_frequency_normalized = cutoff_frequency_seconds / (
			2 * total_time_seconds)  # Normalize frequency (Nyquist = 1)
	return cutoff_frequency_normalized


def get_lp_butter_lp_filter_param(filter_order, cutoff_frequency_normalized):
	# Choose filter type and parameters
	filter_order = filter_order  # Filter order (adjust as needed)
	b, a = signal.butter(filter_order, cutoff_frequency_normalized, btype = 'low', analog = False)  # Butterworth
	# b, a = signal.cheby1(filter_order, 0.1, cutoff_frequency_normalized, btype='low', analog=False) #Chebyshev type 1
	# b, a = signal.bessel(filter_order, cutoff_frequency_normalized, btype='low', analog=False) #Bessel
	return a, b


def lp_filter(a, b, signal):
	# 3. Apply the filter (using lfilter for no phase delay)
	filtered_signal = filtfilt(b, a, signal)
	return filtered_signal


# Or use filtfilt for zero-phase filtering (more computationally intensive, but less phase distortion)
# filtered_values = signal.filtfilt(b, a, values)

def plot_filtering(X, signal, filtered_signal, signal_color,fc_h):
	# --- Plotting ---
	# plt.figure(figsize = (12, 6))

	plt.subplot(2, 1, 1)
	plt.plot(X, signal, label = 'Original upper values', c = signal_color)
	plt.title('Original Data')
	plt.xlabel('Time (days)')
	plt.ylabel('Values')
	plt.legend()

	plt.subplot(2, 1, 2)
	plt.plot(X, filtered_signal, label = 'Filtered upper Values', c = signal_color)
	plt.title(f'Filtered Data ({fc_h}-hour cutoff)')
	plt.xlabel('Time (days)')
	plt.ylabel('Values')
	plt.legend()



if __name__ == "__main__":
	from src.core.glider_survey_profile import extract_curves
	date, cond, depth, lon, lat, pressure, salinity, temp = load_dot_mat_CTD()
	X1, Y1, n = compute_bv_freq(salinity, temp, pressure, lat, date, depth)
	X2, Y2, bv_mean, depth_avg = bv_freq_avg_every_k_meters(n, depth, date)
	upper_boundary, lower_boundary = extract_curves(bv_mean)
	s1 = [depth_avg[e] for e in upper_boundary]
	s2 = [depth_avg[e] for e in lower_boundary]
	del X1, Y1, X2, Y2, n

	fc_h=72

	# s1 and s2 have the same sampling freq and total time
	sf, length_sec = get_sampling_freq_total_time(s1, 14)
	fc = get_cutoff_freq_norm(fc_h, length_sec)
	a, b = get_lp_butter_lp_filter_param(4, fc)
	s1_f = lp_filter(a, b, s1)
	s2_f = lp_filter(a, b, s2)

	plot_filtering(date, s1, s1_f, "red",fc_h)
	plot_filtering(date, s2, s2_f, "blue",fc_h)

	plt.tight_layout()
	plt.show()